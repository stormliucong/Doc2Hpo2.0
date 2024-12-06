import openai
from HpoFactory import search_hpo_in_ncbi
from HpoLookup import HpoLookup

class GptSearch:
    def __init__(self, openai_api_key=None, hpo_lookup=None):
        self.openai_api_key = openai_api_key

    def search_hpo_terms(self,text):
        """
        Search HPO-based phenotype terms in a given text using OpenAI API.

        :param text: The input text to analyze.
        :param hpo_ontology: A dictionary or dataset of HPO terms and their IDs. Format: {term: HPO_ID}.
        :return: A list of dictionaries with 'term', 'start', 'end', and 'hpo_id'.
        """
        # Set up the OpenAI API key
        openai.api_key = self.openai_api_key
        
        # Step 1: Call OpenAI to analyze the text for phenotype terms
        try:
            response = openai.Completion.create(
                engine="gpt-4",
                prompt=(
                    f"Identify all Human Phenotype Ontology (HPO) terms in the following text."
                    f"Do not include negated terms or overlapping terms."
                    f"For each term, provide the start and end positions (start with index 0) of the match in the text. "
                    f'''Example response: [("Abnormal gait", 10, 22),( "Short stature", 30, 43)]\n'''
                    f"Text: \"{text}\""
                ),
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0
            )
            # Extract the terms and positions from the OpenAI response
            matches = response['choices'][0]['text'].strip()
        except Exception as e:
            raise ValueError("Failed to query OpenAI GPT-4.") from e            
        return matches
    
    def post_process_gpts(self, matches):
        '''
        Post-process the GPT-4 output to extract the matched intervals
        '''
         # Step 2: Parse the response (assuming it returns a JSON-like or structured list)
        # Example response: [{"term": "Abnormal gait", "start": 10, "end": 22}, ...]
        try:
            match_list = eval(matches)  # Convert response text to Python list (use with caution)
            intervals = [(match["1"], match["2"]) for match in match_list]
        except Exception as e:
            raise ValueError("Failed to parse OpenAI response.") from e
        return intervals
    
    @staticmethod
    def add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels):
        '''
        Add HPO attributes to the matched intervals
        '''
        matched_hpo = []    
        for start, end in intervals:
            if text[start:end] in hpo_dict:
                hpo_id = hpo_dict[text[start:end]]
                hpo_name = hpo_name_dict[hpo_id]
            else:
                hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi(text[start:end])
                if len(hpo_id_name_format_list) > 1:
                    hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
                if hpo_id_name_format_list:
                    hpo_id = hpo_id_name_format_list["id"]
                    hpo_name = hpo_id_name_format_list["name"]
                else:
                    hpo_id = None
                    hpo_name = None
            matched_hpo.append((start, end, text[start:end], {"id": hpo_id, "name": hpo_name}))
        return matched_hpo   

       
# Example usage
if __name__ == "__main__":
    print("GPT-4 Search")
    from HpoFactory import HpoFactory
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_dict, hpo_name_dict = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    with open('demo_patient_1.txt', 'r') as f:
        text = f.read()
    print(text)
    gpt = GptSearch(openai_api_key="your_openai_api_key_here")
    matches = ac.search(text)
    print("Matches:", matches)
    matched_hpo = ac.add_hpo_attributes(text, matches, hpo_dict, hpo_name_dict)
    print("Matched HPO:", matched_hpo)
