
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
# top 5 match
result_json = './rag_evaluation_query_results_top5_text-embedding-3-large.json'
# load the query results from the json file
with open(result_json, 'r') as f:
    query_results = json.load(f)

# user input key
openai_api_key = input("Enter your OpenAI API key: ")
open_ai_model = 'gpt-4o-2024-08-06'

# convert query_results into pandas dataframe
# Flatten the dictionary
# if not exist file 
if not os.path.exists('nonir_comparison_df.csv'):
        
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
else:
    comparison_df = pd.read_csv('nonir_comparison_df.csv')
    
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
system_message = "Single Choice: Select the best-matching HPO term for the given term based on their definitions. Respond with 1, 2, 3, 4, or 5."

# if not exist folder create a folder
if not os.path.exists('nonir_gpt_response'):
    os.makedirs('nonir_gpt_response')

# loop over unique unique_hp_list
for hp_id in unique_hp_list:
    # check if the file exists
    if os.path.exists(f'nonir_gpt_response/{hp_id}.json'):
        print(f'{hp_id} already exists')
        continue
    print(f'Processing {hp_id}')
    term = comparison_sampled_df[comparison_sampled_df['query_hpo_id'] == hp_id]['query_synonym'].values[0]
    document1 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==0)]["document"].values[0]
    document2 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==1)]["document"].values[0]
    document3 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==2)]["document"].values[0]
    document4 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==3)]["document"].values[0]
    document5 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==4)]["document"].values[0]

    user_message = '''
            term: {term}\n 
            =====================\n
            1. {document1}\n
            2. {document2}\n
            3. {document3}\n
            4. {document4}\n
            5. {document5}\n
            '''.format(
                term=term,
                document1=document1,
                document2=document2,
                document3=document3,
                document4=document4,
                document5=document5
            )
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
        with open(f'nonir_gpt_response/{hp_id}.json', 'w') as f:
            json.dump(output_json, f)
    except Exception as e:
        print(e)
        
# generate prompt for human evaluation
if not os.path.exists('./nonir_human_evaluation'):
    os.makedirs('./nonir_human_evaluation')
# loop over unique unique_hp_list
row = []
for hp_id in unique_hp_list:
    print(f'Processing {hp_id}')
    term = comparison_sampled_df[comparison_sampled_df['query_hpo_id'] == hp_id]['query_synonym'].values[0]
    document1 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==0)]["document"].values[0]
    document2 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==1)]["document"].values[0]
    document3 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==2)]["document"].values[0]
    document4 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==3)]["document"].values[0]
    document5 = comparison_sampled_df[(comparison_sampled_df['query_hpo_id'] == hp_id) & (comparison_sampled_df['top_k'] ==4)]["document"].values[0]

    user_message = '''
            term: {term}\n 
            =====================\n
            1. {document1}\n
            2. {document2}\n
            3. {document3}\n
            4. {document4}\n
            5. {document5}\n
            '''.format(
                term=term,
                document1=document1,
                document2=document2,
                document3=document3,
                document4=document4,
                document5=document5
            )
    with open(f'nonir_human_evaluation/{hp_id}.txt', 'w') as f:
        f.write(user_message)
    row.append({"query_hpo_id": hp_id, "query_synonym": term})

# write to a csv file
human_evaluation_worksheet_df = pd.DataFrame(row)
human_evaluation_worksheet_df['rank_1'] = ''
human_evaluation_worksheet_df['rank_2'] = ''
human_evaluation_worksheet_df['rank_3'] = ''
human_evaluation_worksheet_df['rank_4'] = ''
human_evaluation_worksheet_df['rank_5'] = ''
human_evaluation_worksheet_df.to_csv('nonir_human_evaluation_worksheet.csv', index=False)


    


