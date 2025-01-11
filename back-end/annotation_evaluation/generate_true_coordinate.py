
import sys
sys.path.append('..')
from HpoFactory import HpoFactory
from AhoCorasickSearch import AhoCorasick
from ScispacySearch import ScispacySearch
from HpoLookup import HpoLookup
from GptSearch import GptSearch
import warnings
warnings.filterwarnings("ignore")
import glob
import json
import os

# Initialize HPO Factory
hpo_F = HpoFactory(hpo_file = '../hp.obo')
hpo_tree = hpo_F.build_hpo_tree()
hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
hpo_dict, hpo_name_dict, _ = hpo_F.build_hpo_dict(hpo_ancestors)
hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)

# Initialize Aho-Corasick
ac = AhoCorasick(hpo_dict)

# Initialize Scispacy
# scispacy = ScispacySearch()

gpt = GptSearch()

# if not exist, create a folder to store the updated json files
if not os.path.exists('./simulated_pt_coordinate'):
    os.makedirs('./simulated_pt_coordinate')

# load json files
file_list = glob.glob('./simulated_pt_description/*.json')
for file in file_list:
    output = os.path.join('./simulated_pt_coordinate', os.path.basename(file))
    # if not exist
    if os.path.exists(output):
        # load file and check 'ac' and 'gpt' keys
        with open(output, 'r') as f:
            json_data = json.load(f)
            if 'ac' in json_data['matched_hpo'] and 'gpt' in json_data['matched_hpo']:
                print(f"{output} already exists")
                continue
    else:
        with open(file, 'r') as f:
            print(f"Processing {file}")
            json_data = json.load(f)
            text = json_data['response']
            json_data['matched_hpo'] = {}
            # Aho-Corasick
            try:
                intervals, terms = ac.search(text)
                json_data['matched_hpo']['ac'] = {"terms": terms, "intervals": intervals}
            except:
                print("Aho-Corasick failed")
            
            # # GPT-4
            try:
                gpt_response = gpt.search_hpo_terms(text, test=False)
                intervals, gpt_response_hpo_terms = gpt.post_process_gpts(gpt_response)
                json_data['matched_hpo']['gpt'] = {"terms": gpt_response_hpo_terms, "intervals": intervals}
            except:
                print("GPT-4 failed")
            # # Save the updated json file
            with open(output, 'w') as f:
                json.dump(json_data, f, indent=4)

            






