from openai import OpenAI
from pydantic import BaseModel
import json

class Interval(BaseModel):
    start: int
    end: int
    substring: str
    hpo_id: str
    hpo_name: str
    
class Intervals(BaseModel):
    results: list[Interval]
    
class Findings(BaseModel):
    findings: list[str]

class GptSearch:
    def __init__(self, model="gpt-4o-2024-08-06",openai_api_key=None):
        if openai_api_key is None:
            user_input = input("Enter your OpenAI API key: ")
            if len(user_input) > 0:
                self.openai_api_key = user_input
            else:
                raise ValueError("OpenAI API key is required.")
        else:
            self.openai_api_key = openai_api_key
        
        self.model = model
        
    def search_clinical_findings(self,text, test=False):
        
        system_message = '''
        Carefully review every sentence of the clinical passage to identify terms related to 
        genetic inheritance patterns, anatomical anomalies, clinical symptoms, diagnostic findings, 
        test results, and specific conditions or syndromes. Completely ignore negative findings, normal 
        findings (i.e. 'normal' or 'no'), procedures and family history. Include appropriate context 
        based only on the passage. Return the extracted terms in a JSON object 
        with a single key 'findings', which contains the list of extracted terms spelled correctly. 
        Ensure the output is concise without any additional notes, commentary, or meta explanations.
        '''
        user_message = f'''
            {text}\n
        '''
        # Step 1: Call OpenAI to analyze the text for phenotype terms
        try:
            client = OpenAI(api_key=self.openai_api_key)
            completion = client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content":  system_message},
                    {"role": "user", "content": user_message}
                ],
                max_completion_tokens = 1024,
                temperature = 0.8,
                response_format=Findings,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0
            )
            
            # Extract the terms and positions from the OpenAI response
            # output completion to a file
            with open('gpt_response.json', 'w') as f:
                f.write(str(completion))
                
            gpt_response = completion.choices[0].message.parsed
            findings = gpt_response.dict().get("findings", [])
            return findings
        except Exception as e:
            raise ValueError(f"Failed to query OpenAI {self.model}.\n Check your OpenAI Key. \n" + str(e))       

    def post_process_findings(self, text, findings):
        '''
        find the most likely matched phrase based on string.
        '''
        results = []
        # split the text into sentences
        sentences = text.split(".")
        matched_findings = []
        max_matching_tokens = 0
        max_common_tokens = ''
        for finding in findings:
            for sentence in sentences:
                # check the finding tokens and sentence token match rate
                sentence_tokens = sentence.lower().split(" ")
                finding_tokens = finding.lower().split(" ")
                common_tokens = set(sentence_tokens).intersection(set(finding_tokens))
                if len(common_tokens) > max_matching_tokens:
                    max_matching_tokens = len(common_tokens)
                    # calculate the start and end position of the matched phrase
                    max_common_tokens = common_tokens
                    best_match_sentence = sentence  # Store the sentence with the most matching words
            matched_findings.append(best_match_sentence)

            for bms in matched_findings:
                sentence_start = text.find(bms)
                token_start = bms.lower().find(" ".join(common_tokens).lower())
                text_start = sentence_start + token_start
                text_end = text_start + len(" ".join(common_tokens))
                results.append({"start": text_start, "end": text_end, "substring": text[text_start:text_end], "phrase": finding})
            
            if len(results) > 0:
                # convert results to interval list and phrase list
                intervals = [(match["start"], match["end"]) for match in results]
                terms = [match["phrase"] for match in results]
            else:
                return None, None
        return intervals, terms            
    
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
        
        system_message = '''
            Identify all Human Phenotype Ontology (HPO) terms in the following text.\n
            1. For each identified phenotype, provide the start and end positions of the substring in the text indicating this phenotype.\n
            2. Do not include negated phenotypes.\n
            3. Do not include substrings overlapping with other substrings.\n
            4. Return a list of JSON objects with the following keys: 'start', 'end', 'substring', 'hpo_name', 'hpo_id'.\n
            --------------------------------------------------------------------------------------------\n
        '''
        
        user_message = f'''
            {text}\n
        '''
                         
        # Step 1: Call OpenAI to analyze the text for phenotype terms
        try:
            client = OpenAI(api_key=self.openai_api_key)
            completion = client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content":  system_message},
                    {"role": "user", "content": user_message}
                ],
                max_completion_tokens = 1024,
                temperature = 0.8,
                response_format=Intervals,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0
            )
            
            # Extract the terms and positions from the OpenAI response
            # output completion to a file
            with open('gpt_response.json', 'w') as f:
                f.write(str(completion))
                
            gpt_response = completion.choices[0].message.parsed
            return gpt_response
        except Exception as e:
            raise ValueError(f"Failed to query OpenAI {self.model}.\n Check your OpenAI Key. \n" + str(e))       
    
    def post_process_gpts(self, response):
        '''
        Post-process the GPT-4 output to extract the matched intervals
        '''
         # Step 2: Parse the response (assuming it returns a JSON-like or structured list)
        # Example response: [{"term": "Abnormal gait", "start": 10, "end": 22}, ...]
        try:
            results_dict = response.dict()["results"]
            # match_list = json.loads(gpt_response)
            intervals = [(match["start"], match["end"]) for match in results_dict]
            hpo_terms = [match["hpo_name"] for match in results_dict]
            return intervals, hpo_terms
        except Exception as e:
            raise ValueError("Failed to parse GPT response.\n" + str(e)) 
        

       
# Example usage
if __name__ == "__main__":
    print("GPT-4 Search")
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
    gpt = GptSearch()
    gpt_response = gpt.search_hpo_terms(text, test=False)
    intervals, gpt_response_hpo_terms = gpt.post_process_gpts(gpt_response)
    print("Intervals:", intervals, "HPO Terms:", gpt_response_hpo_terms)
    # matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, response_hpo_terms=gpt_response_hpo_terms)
    # print("Matched HPO:", matched_hpo)
    findings = gpt.search_clinical_findings(text, test=False)
    intervals, terms = gpt.post_process_findings(text, findings)
    print("Intervals:", intervals, "Terms:", terms)
    matched_hpo = HpoLookup.add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, response_hpo_terms=terms)
    print("Matched HPO:", matched_hpo)