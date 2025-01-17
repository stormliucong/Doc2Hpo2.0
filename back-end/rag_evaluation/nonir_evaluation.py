
from openai import OpenAI
from pydantic import BaseModel
import os
import json
import requests
import time
import pandas as pd
import numpy as np
import re
# import modules in the parent directory
import sys
sys.path.append('..')
from HpoDatabase import HpoDatabase


class Choice(BaseModel):
    choice: int
    
# prepare HPO dict
db_path = '../hpo_chroma_db'
obo_path = '../hp.obo'
hpo_db = HpoDatabase(obo_path=obo_path, db_path=db_path, woosh_path=None, embedding_model=None)
hpo_object_list = hpo_db.parse_obo(obo_path)
hpo_object_df = pd.DataFrame(hpo_object_list)

# Load rag_evaluation
# top x match
x = 25
result_json = f'./rag_evaluation_query_results_top{x}_text-embedding-3-large.json'
# load the query results from the json file
with open(result_json, 'r') as f:
    query_results = json.load(f)

# user input key
openai_api_key = input("Enter your OpenAI API key: ")
open_ai_model = 'gpt-4o-2024-08-06'

# convert query_results into pandas dataframe
# Flatten the dictionary
# if not exist file 
if not os.path.exists(f'nonir_comparison_df_top{x}.csv'):
        
    rows = []
    for key, value in query_results.items():
        for entry in value:
            synonym = entry.get('synonym', '')
            for result in entry.get('parsed_results', []):
                hp_id = result['hpo_id']
                document = hpo_object_df[hpo_object_df['id'] == hp_id]['document'].values[0]
                rows.append({
                    'query_hpo_id': key,
                    'query_synonym': synonym,
                    'hit_hpo_id': result['hpo_id'],
                    'hit_hpo_name': result['hpo_name'],
                    'top_k': result['top_k'],
                    'distance': result['distance'],
                    'document': document
                })

    comparison_df = pd.DataFrame(rows)
    comparison_df.to_csv(f'nonir_comparison_df_top{x}.csv', index=False)
else:
    comparison_df = pd.read_csv(f'nonir_comparison_df_top{x}.csv')
    
# subset hit correct with top 5
matched_df = comparison_df[comparison_df['hit_hpo_id'] == comparison_df['query_hpo_id']]
# get unique query_hpo_id
query_hpo_id_list = matched_df['query_hpo_id'].unique()
# sample 100 query_hpo_id
# set a seed
np.random.seed(0)
query_hpo_id_list = np.random.choice(query_hpo_id_list, 100, replace=False)
# subset matched_df by query_hpo_id
matched_df = matched_df[matched_df['query_hpo_id'].isin(query_hpo_id_list)]
# for each query_hpo_id, sample 1 query_synonym
query_hpo_synonym_list = matched_df.groupby('query_hpo_id').apply(lambda x: x.sample(1))
# sample 100 query_synonym_id_list
query_synonym_id_list = query_hpo_synonym_list.sample(n=100)
# subset the comparison_df by query_synonym, and query_hpo_id
comparison_sampled_df = comparison_df[comparison_df['query_synonym'].isin(query_synonym_id_list['query_synonym']) & comparison_df['query_hpo_id'].isin(query_synonym_id_list['query_hpo_id'])]
# unique hp_list
unique_hp_list = comparison_sampled_df['query_hpo_id'].unique()

# openai client
client = OpenAI(api_key=openai_api_key)
x_string = ', '.join([str(i+1) for i in range(x-1)]) + ' or ' + str(x)
system_message = "Single Choice: Select the best-matching HPO term for the given term based on their definitions. Respond with {x_string}."

# if not exist folder create a folder
if not os.path.exists(f'nonir_gpt_response_top{x}'):
    os.makedirs(f'nonir_gpt_response_top{x}')

# loop over unique unique_hp_list
for hp_id in unique_hp_list:
    # check if the file exists
    if os.path.exists(f'nonir_gpt_response_top{x}/{hp_id}.json'):
        print(f'{hp_id} already exists')
        continue
    print(f'Processing {hp_id}')
    term = comparison_sampled_df[comparison_sampled_df['query_hpo_id'] == hp_id]['query_synonym'].values[0]
    document_list = [comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] == i)]["document"].values[0] for i in range(x)]

    user_message = '''
            term: {term}\n 
            =====================\n
            ''' + '\n'.join([f'{i+1}. {document}' for i, document in enumerate(document_list)]) + '\n'
    try:
        completion = client.beta.chat.completions.parse(
            model=open_ai_model,
            messages=[
                {"role": "system", "content":  system_message},
                {"role": "user", "content": user_message}
            ],
            max_completion_tokens = 1024,
            temperature = 0.8,
            response_format=Choice,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0
        )
        gpt_response = completion.choices[0].message.parsed
        results_choice= gpt_response.dict()["choice"]
        
        output_json = {}
        output_json['query_hpo_id'] = hp_id
        output_json['query_synonym'] = term
        output_json['gpt_response'] = results_choice
        output_json['gpt_hit_hpo_id'] = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==(results_choice - 1))]["hit_hpo_id"].values[0]
        # write results to a json file
        with open(f'nonir_gpt_response_top{x}/{hp_id}.json', 'w') as f:
            json.dump(output_json, f)
    except Exception as e:
        print(e)
        
# generate prompt for human evaluation
if not os.path.exists('./nonir_human_evaluation'):
    os.makedirs('./nonir_human_evaluation')
# loop over unique unique_hp_list
row = []
for hp_id in unique_hp_list[0:5]:
    print(f'Processing {hp_id}')
    term = comparison_sampled_df[comparison_sampled_df['query_hpo_id'] == hp_id]['query_synonym'].values[0]
    document_list = [comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] == i)]["document"].values[0] for i in range(x)]
    user_message = '''
            term: {term}\n 
            =====================\n
            ''' + '\n'.join([f'{i+1}. {document}' for i, document in enumerate(document_list)]) + '\n' 
    # with open(f'nonir_human_evaluation/{hp_id}.txt', 'w') as f:
    #     f.write(user_message)
    row.append({"query_hpo_id": hp_id, "query_synonym": term, "question": user_message})

# write to a csv file
human_evaluation_worksheet_df = pd.DataFrame(row)
for i in range(x):
    human_evaluation_worksheet_df[f'rank_{i+1}'] = ''
human_evaluation_worksheet_df.to_csv(f'nonir_human_evaluation_worksheet_top{x}.csv', index=False)


    


