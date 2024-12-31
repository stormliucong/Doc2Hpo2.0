# import modules in the parent directory
import sys
sys.path.append('..')
from HpoDatabase import HpoDatabase
import os
import json
import random

db_path = '../hpo_chroma_db'
obo_path = '../hp.obo'
hpo_db = HpoDatabase(db_path, obo_path)
# # test query
# query = "muscle weakness"
# results = hpo_db.query_hpo(query)
# hpo_id, hpo_name = hpo_db.parse_results(results)
# print(hpo_id, hpo_name)


# load all synonyms generated by GPT-4o-mini
synonym_folder = '/Users/cl3720/Desktop/hpo-parser-fine-tuned-gemini/hpo_synonyms/gpt-4o-mini-2024-07-18'

expanded_hpo_name_dict = {}
if os.path.exists(synonym_folder):
# load the synonyms from the folder
# each file in the folder is a json file with the following format {"HP:XXXX": ["synonym1", "synonym2", "synonym3"]}
    for file in os.listdir(synonym_folder):
        with open(os.path.join(synonym_folder, file), "r") as f:
            expanded_hpo_name_dict.update(json.load(f))
print(f"There are {len(expanded_hpo_name_dict)} HPO terms with synonyms")


# query with synonyms and store the id.
query_results = {}
i = 0
for hp_id in expanded_hpo_name_dict:
    i += 1
    if i % 1000 == 0:
        print(f"Processed {i} HPO terms")       
    
    if i > 100:
        break   
    query_results[hp_id] = []
    for synonym in expanded_hpo_name_dict[hp_id]:
        # p = random.random()
        # create a random indicator p (0,1) to decide whether to query the synonym
        # for testing purposes onlyl.
        # takes ~5 minutes to query 500 HPO terms
        # on average, it takes 0.6 seconds to query one HPO term
        # so it will take 0.6 * 18000 / 3600 = 3 hours to query all HPO terms
        # if p > 0.01:
        #     continue
        results = hpo_db.query_hpo(synonym, n_results=5)
        parsed_results = hpo_db.parse_results_n_results(results)
        
        query_results[hp_id].append({"synonym": synonym, "parsed_results": parsed_results})
print(f"Finished querying {i} HPO terms")

# write the query results to a json file
with open('./rag_evaluation_query_results_top5_default.json', 'w') as f:
    json.dump(query_results, f)
    
print("Query results saved to rag_evaluation_query_results_top5_default.json")