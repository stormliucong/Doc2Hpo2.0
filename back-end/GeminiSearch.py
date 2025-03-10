import google.generativeai as genai
import typing_extensions as typing
import ast
from pydantic import BaseModel


import typing_extensions as typing

class Interval(BaseModel):
    start: int
    end: int
    substring: str
    hpo_id: str
    hpo_name: str
    
class Intervals(BaseModel):
    results: list[Interval]


class GeminiSearch:
    def __init__(self, api_key=None, model_id="gemini-2.0-flash-exp"):
        if api_key is None:
            api_key = input("Enter your Gemini API key: ")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_id)
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_id)
            
            
    def run_gemini(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
        
    def run_gemini_json(self, prompt, response_schema=list[Interval]):
        response = self.model.generate_content(prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=response_schema))
        string_list = response.text
        list_string = ast.literal_eval(string_list)
        print(list_string)
        return list_string
    
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

        prompt = '''
            Identify all Human Phenotype Ontology (HPO) terms in the following text.\n
            1. For each identified phenotype, provide the start and end positions of the substring in the text indicating this phenotype.\n
            2. Do not include negated phenotypes.\n
            3. Do not include substrings overlapping with other substrings.\n
            4. Return a list of JSON objects with the following keys: 'start', 'end', 'substring', 'hpo_name', 'hpo_id'.\n
            --------------------------------------------------------------------------------------------\n
        '''
        prompt += text
        response = self.run_gemini_json(prompt, response_schema=Intervals)
        with open('gemini_response.json', 'w') as f:
            f.write(str(response))    
            return response
        
    def post_process_gemini(self, response):
        '''
        Post-process the Gemini output to extract the matched intervals
        '''
        # Step 2: Parse the response (assuming it returns a JSON-like or structured list)
        # Example response: [{"term": "Abnormal gait", "start": 10, "end": 22}, ...]
        try:
            intervals = []
            hpo_terms = []
            
            
            response = response['results']
            
            for match in response:
                if 'start' in match:
                    start = int(match['start'])
                    if 'end' in match:
                        end = int(match['end'])
                    elif "substring" in match:
                        end = start + len(match['substring'])
                    else:
                        continue
                else:
                    continue 
                
                if 'hpo_name' in match:
                    hpo_name = match['hpo_name']
                elif 'substring' in match:
                    hpo_name = match['substring']
                else:
                    continue

                intervals.append((start, end))
                hpo_terms.append(hpo_name)
                
            return intervals, hpo_terms
        except Exception as e:
            raise ValueError("Failed to parse Gemini response.\n" + str(e)) 
       
    
    
# Example usage
if __name__ == "__main__":
    print("Gemini Search")
    from HpoFactory import HpoFactory
    from HpoLookup import HpoLookup
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    hpo_dict, hpo_name_dict, _ = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    with open('demo_patient_1.txt', 'r') as f:
        text = f.read()
    print(text)
    gemini = GeminiSearch()
    response = gemini.search_hpo_terms(text, test=False)
    intervals = gemini.post_process_gemini(response)
    matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels)
    print("Matched HPO:", matched_hpo)