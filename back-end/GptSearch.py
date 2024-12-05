import openai

class GptSearch:
    def __init__(self, openai_api_key=None):
        self.openai_api_key = openai_api_key

    def search_hpo_terms(self,text, hpo_dict):
        """
        Search HPO-based phenotype terms in a given text using OpenAI API.

        :param text: The input text to analyze.
        :param hpo_ontology: A dictionary or dataset of HPO terms and their IDs. Format: {term: HPO_ID}.
        :return: A list of dictionaries with 'term', 'start', 'end', and 'hpo_id'.
        """
        # Set up the OpenAI API key
        openai.api_key = self.openai_api_key

        # Step 1: Call OpenAI to analyze the text for phenotype terms
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=(
                f"Identify all Human Phenotype Ontology (HPO) terms in the following text."
                f"Do not include negated terms or overlapping terms."
                f"For each term, provide the start and end positions of the match in the text. "
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
        return matches
    
    def post_process_gpts(self, matches):
        '''
        Post-process the GPT-4 output to extract the matched intervals
        '''
         # Step 2: Parse the response (assuming it returns a JSON-like or structured list)
        # Example response: [{"term": "Abnormal gait", "start": 10, "end": 22}, ...]
        try:
            match_list = eval(matches)  # Convert response text to Python list (use with caution)
            intervals = [(match["start"], match["end"]) for match in match_list]
        except Exception as e:
            raise ValueError("Failed to parse OpenAI response.") from e
        return intervals
    
    def add_hpo_attributes(self, text, intervals, hpo_dict):
        '''
        Add HPO attributes to the matched intervals
        '''
        # return empty value for key not in the dict.        
        matched_hpo = [(start, end, text[start:end], hpo_dict[text[start:end]] ) for start, end in intervals]
        return matched_hpo    

       
# Example usage
if __name__ == "__main__":
    # Example HPO ontology (you can use a real dataset here)
    hpo_ontology = {
        "Abnormal gait": "HP:0001288",
        "Short stature": "HP:0004322",
        "Cleft palate": "HP:0000175"
    }

    # Example text to analyze
    text = "The patient exhibits abnormal gait and cleft palate."

    # Call the function with your OpenAI API key
    openai_api_key = "your_openai_api_key"
    results = search_hpo_terms(text, openai_api_key, hpo_ontology)

    # Print the results
    print(results)
