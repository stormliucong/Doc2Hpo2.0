from openai import OpenAI

class GptSearch:
    def __init__(self, model="gpt-3.5-turbo",openai_api_key=None):
        if openai_api_key is None:
            user_input = input("Enter your OpenAI API key: ")
            if len(user_input) > 0:
                self.openai_api_key = user_input
            else:
                raise ValueError("OpenAI API key is required.")
        else:
            self.openai_api_key = openai_api_key
        
        self.model = model

    def search_hpo_terms(self,text, test=False):
        """
        Search HPO-based phenotype terms in a given text using OpenAI API.

        :param text: The input text to analyze.
        :param hpo_ontology: A dictionary or dataset of HPO terms and their IDs. Format: {term: HPO_ID}.
        :return: A list of dictionaries with 'term', 'start', 'end', and 'hpo_id'.
        """
        # Set up the OpenAI API key
        if test:
            return f'[(10, 22, "Abnormal gait",),(30, 43, "Short stature")]'
        

        system_message = f'''
            Identify all Human Phenotype Ontology (HPO) terms in the following text.
            Do not include negated terms or overlapping terms.
            For each term, provide the start and end positions of the snippet in the text containing the term or its synonyms or descriptions showing the phenotype.
            Do not overlap the start and end positions of the snippets.
            Use the following json format for return: [(start, end, \"term\"), ...].
            Return the response in one line, don't include "\\n".
            Example response: [(10, 22, "Abnormal gait",),(30, 43, "Short stature")]\n
        '''
        
        user_message = f'''
            Text: \"{text}\"
        '''
                         
        # Step 1: Call OpenAI to analyze the text for phenotype terms
        try:
            client = OpenAI(api_key=self.openai_api_key)
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content":  system_message},
                    {"role": "user", "content": user_message}
                ],
                max_completion_tokens = 1024,
                temperature = 0.8,
                # response_format = { "type": "json_object" },
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0
            )
            
            # Extract the terms and positions from the OpenAI response
            # output completion to a file
            with open('gpt_response.json', 'w') as f:
                f.write(str(completion))
                
            gpt_response = completion.choices[0].message.content
            print(gpt_response)
        except Exception as e:
            raise ValueError(f"Failed to query OpenAI {self.model}.") from e            
        return gpt_response
    
    def post_process_gpts(self, gpt_response):
        '''
        Post-process the GPT-4 output to extract the matched intervals
        '''
         # Step 2: Parse the response (assuming it returns a JSON-like or structured list)
        # Example response: [{"term": "Abnormal gait", "start": 10, "end": 22}, ...]
        try:
            # match_list = json.loads(gpt_response)
            match_list = eval(gpt_response)  # Convert response text to Python list (use with caution)
            intervals = [(match[0], match[1]) for match in match_list]
            gpt_response_hpo_terms = [match[2] for match in match_list]
            print(intervals)
        except Exception as e:
            raise ValueError("Failed to parse OpenAI response.") from e
        return intervals, gpt_response_hpo_terms

       
# Example usage
if __name__ == "__main__":
    print("GPT-4 Search")
    from HpoFactory import HpoFactory
    from HpoLookup import HpoLookup
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    hpo_dict, hpo_name_dict = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    with open('demo_patient_1.txt', 'r') as f:
        text = f.read()
    print(text)
    gpt = GptSearch()
    gpt_response = gpt.search_hpo_terms(text, test=True)
    intervals, gpt_response_hpo_terms = gpt.post_process_gpts(gpt_response)
    matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, gpt_response_hpo_terms)
    print("Matched HPO:", matched_hpo)
