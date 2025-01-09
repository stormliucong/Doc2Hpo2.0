import google.generativeai as genai
from HpoFactory import HpoFactory
from HpoLookup import HpoLookup
from ScispacySearch import ScispacySearch
import os
import uuid 
import json

class TextSimulator:
    def __init__(self, gemini_api_key=None, gemini_model_id="gemini-1.5-flash", hpo_terms=None, output_dir=None):
        if gemini_api_key is None:
            gemini_api_key = input("Enter your Gemini API key: ")
        
        if output_dir is None:
            output_dir = "training_dataset"
            os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel(gemini_model_id)
        self.hpo_F = HpoFactory()
        self.hpo_tree = self.hpo_F.build_hpo_tree()
        self.hpo_ancestors = self.hpo_F.get_hpo_ancestors(self.hpo_tree)
        self.hpo_levels = self.hpo_F.get_hpo_levels(self.hpo_tree)
        self.hpo_dict, self.hpo_name_dict = self.hpo_F.build_hpo_dict(self.hpo_ancestors)
        self.hpo_dict = self.hpo_F.expand_hpo_dict(self.hpo_dict)
        self.scispacy = ScispacySearch()
        
    def run(self):
        '''
        Run the Text Simulator
        '''
        hpo_terms = ["Abnormality of the dentition", "Abnormality of the jaw", "Abnormality of the teeth", "Abnormality of the face"]
        gemini_response = self.get_text_from_gemini(hpo_terms = hpo_terms)
        print("Gemini Response:", gemini_response)
        matched_hpo = self.parse_by_scispacy(gemini_response)
        print("Matched HPO:", matched_hpo)
        substitute_text, hpo_substitutions = self.substitute_and_update_positions(gemini_response, matched_hpo)
        synonym_substitutions = self.get_synonyms_from_gemini(hpo_substitutions)
        for synonym_substitution in synonym_substitutions:
            input, output = self.substitute_and_update_positions(substitute_text, synonym_substitution)
            # create a json file with input, output, 
            # Save the hpo_terms, gemini_response, matched_hpo, substitute_text, hpo_substitutions, synonym_substitutions in a json file
            # save input and output in a json file
            detailed_json = {"hpo_terms": hpo_terms, "gemini_response": gemini_response, "matched_hpo": matched_hpo, "substitute_text": substitute_text, "hpo_substitutions": hpo_substitutions, "synonym_substitutions": synonym_substitutions}
            dataset_json = {"input": input, "output": output}
            file_id = uuid.uuid4()
            with open(os.path.join(self.output_dir, f"{file_id}_detailed.json"), "w") as f:
                json.dump(detailed_json, f)
            with open(os.path.join(self.output_dir, f"{file_id}_dataset.json"), "w") as f:
                json.dump(dataset_json, f)
         
    def get_text_from_gemini(self, hpo_terms=None):
        '''
        Get the response from Gemini API
        '''
        # create api key here.
        # https://aistudio.google.com/app/apikey
        if hpo_terms is None:
            hpo_terms = ["Abnormality of the dentition", "Abnormality of the jaw", "Abnormality of the teeth", "Abnormality of the face"]
        terms = ";".join(hpo_terms) # add the HPO terms here
        prompt = f'''
        Generate a faked clinical notes for a rare genetic disorder patients. 
        1. It should contain a brief description of the patient's symptoms and medical history.
        2. It should contain various phenotype terms from HPO vocabulary. 
        3. It should at least contain the following terms {terms}.
        4. Do not explicitly mention the HPO vocabulary.
        5. Do not include planning, treatment, or any other future-oriented information.
        6. The length of the text should be around 500-1000 words.
        '''
        response = self.model.generate_content(prompt)
        return response.text
    
    def get_synonyms_from_gemini(self, matched_hpo):
        '''
        Get the synonyms from Gemini API
        '''
        for hpo in matched_hpo:
            hpo_name = hpo[3]["name"]
            prompt = f'''
            Generate synonyms for the HPO term: {hpo_name}. Return at least 5 synonyms in a list.
            Example: Synonyms for the term "Abnormality of the dentition" are ["Dental abnormalities", "Tooth abnormalities", "Dentition abnormalities", "Dental anomalies", "Tooth anomalies"]
            '''
            response = self.model.generate_content(prompt)
            print(response.text)
            try:
                synonym_list = eval(response.text)
            except Exception as e:
                print("Failed to evaluate the response from Gemini.")
                print(e)
                continue
            synonym_substitutions = []
            for synonym in synonym_list:
                synonym_substitutions.append((hpo[0], hpo[1], hpo[2], {"id": hpo[3]["id"], "name": synonym}))
            return synonym_substitutions
    
    def parse_by_scispacy(self, gemini_text):
        '''
        Parse the text using ScispacySearch
        '''
        intervals, linked_hpo_names = self.scispacy.search(gemini_text)
        print("Intervals:", intervals)
        print("Linked HPO Names:", linked_hpo_names)
        matched_hpo = HpoLookup.add_hpo_attributes(gemini_text, intervals, self.hpo_dict, self.hpo_name_dict, self.hpo_levels, linked_hpo_names)
        return matched_hpo

    def substitute_and_update_positions(self, text, substitutions):
        """
        Substitute substrings in the text based on start, end positions and substitute_string.
        Updates the start and end positions for the substitutions.

        Args:
            text (str): The original text.
            substitutions (list  of tuple): A list of tuples containing
                - start (int): The starting index of the substring to be replaced.
                - end (int): The ending index (exclusive) of the substring to be replaced.
                - hpoAttribute (dict): The HPO attribute to substitute the substring with.

        Returns:
            str: The modified text.
            list of dict: The updated substitutions with adjusted start and end positions.
        """
        # Sort the substitutions by their start positions in reverse order to avoid conflicts
        substitutions.sort(key=lambda x: x[0], reverse=True)
        substitutions = [list(tup) for tup in substitutions]

        current_index = 0
        for substitution in substitutions:
            try:
                start = substitution[0]
                end = substitution[1]
                substitute_string = substitution[3]['name'] # hpo_name
                if start < 0 or end > len(text):
                    current_index += 1
                    continue
            except KeyError:
                continue
            
            # Perform the substitution
            text = text[:start] + substitute_string + text[end:]
            # Update the end position
            new_end = start + len(substitute_string)
            # Update the substitution dictionary
            substitution[1] = new_end # TypeError: 'tuple' object does not support item assignment
            
            # Update subsequent substitutions to reflect changes in text length
            length_change = len(substitute_string) - (end - start)

            
            for other_substitution in substitutions[current_index:]:
                if other_substitution[0] > start:
                    # Should not happen
                    raise ValueError("Substitution start position is greater than the current substitution.\n Start: {}\n Substitution: {}\n Current Substitution: {}".format(start, substitution, other_substitution))

            current_index += 1
        # Re-sort substitutions based on updated start positions (optional, for consistency)
        substitutions.sort(key=lambda x: x[0])
        
        substitutions = [tuple(lst) for lst in substitutions]

        return text, substitutions

# Example usage
if __name__ == "__main__":
    # text_simulator = TextSimulator()
    # gemini_response = text_simulator.get_gemini_response()
    # print("Gemini Response:", gemini_response)
    # matched_hpo = text_simulator.parse_by_scispacy(gemini_response)
    # print("Matched HPO:", matched_hpo)
    # print("Substitute and Update Positions")
    # text = "Hello world!"
    # substitutions = [
    #     (6, 11, "",{"id":123,"name": "universe"}),
    #     (0, 5, "",{"id":123,"name": "Hi"})
    # ]
    # text_simulator = TextSimulator()
    # modified_text, updated_substitutions = text_simulator.substitute_and_update_positions(text, substitutions)
    # print("Modified Text:", modified_text)
    # print("Updated Substitutions:", updated_substitutions)
    # assert modified_text == "Hi universe!"
    
    text_simulator = TextSimulator()
    text_simulator.run()
    
