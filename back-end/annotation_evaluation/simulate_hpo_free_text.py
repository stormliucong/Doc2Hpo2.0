import google.generativeai as genai
import json
# import modules in the parent directory
import sys
sys.path.append('..')
from HpoFactory import HpoFactory
import random
import uuid 
import time
# create api key here.
# https://aistudio.google.com/app/apikey
api_key = input("Enter your Gemini API key: ")
genai.configure(api_key=api_key)
model_id = "gemini-1.5-flash"
model = genai.GenerativeModel(model_id)

hpoF = HpoFactory(hpo_file="../hp.obo")
hpo_tree = hpoF.build_hpo_tree()
hpo_ancestors = hpoF.get_hpo_ancestors(hpo_tree)
hpo_levels = hpoF.get_hpo_levels(hpo_tree)
hpo_dict, hpo_name_dict, hpo_synonym_dict = hpoF.build_hpo_dict(hpo_ancestors)
hpo_dict = hpoF.expand_hpo_dict(hpo_dict)

hpo_id_set = list(hpo_dict.keys())
i = 0
while True:
    i+=1
    time.sleep(10)
    if i > 100:
        break
    # randomly sample 5 HPO terms
    hpo_terms_idx = random.sample(range(0, len(hpo_id_set)), 5)
    hpo_terms = [hpo_id_set[i] for i in hpo_terms_idx]
    hpo_ids = [hpo_dict[hpo_term] for hpo_term in hpo_terms]
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
    try:
        response = model.generate_content(prompt)
        json_data = {"model_id": model_id, "hpo_terms": hpo_terms, 'hpo_ids': hpo_ids, "prompt": prompt, "response": response.text}
        # save the model_id, terms, prompts, and response to a json file
        file_name = f"./simulated_pt_description/{uuid.uuid4()}.json"
        with open(file_name, "w") as f:
            json.dump(json_data, f)
    except Exception as e: 
        print(f"Failed to generate content. {e}")
