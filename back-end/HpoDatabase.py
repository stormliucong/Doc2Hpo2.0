# This file is a pipeline to parse hp.obo, and break each HPO term into a JSON file.
# The JSON file is then used to search for HPO terms in a given text using OpenAI API.
# The pipeline is as follows:
# 1. Parse hp.obo file to extract HPO terms, HPO synonyms, and HPO definitions, and their IDs.
# 2. Create a JSON file for each HPO term with the following keys: 'term', 'synonyms', 'definition', and 'hpo_id'.
# 3. Use ChromaDB to index the JSON files.
# 4. Search for HPO terms in a given text using OpenAI API.

# Import the necessary libraries
import os
import json
import re
import requests
from collections import defaultdict
from typing import List
from HpoFactory import HpoFactory
import chromadb
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import time
import threading
from whoosh.collectors import TimeLimitCollector, TimeLimit
import chromadb.utils.embedding_functions as embedding_functions


# Define the HPO database class
class HpoDatabase:
    def __init__(self, obo_path, db_path=None, woosh_path=None, embedding_model=None):
        self.obo_path = obo_path
        self.whoosh_path = woosh_path
        if woosh_path is None:
            self.use_chromdb = True
            self.chromadb_client = chromadb.PersistentClient(path=db_path)
            if embedding_model is None:
                self.ef = None
                self.embedding_model = None
            elif embedding_model == 'text-embedding-3-small':
                openai_api_key = input("Enter your OpenAI API key: ")
                self.ef = embedding_functions.OpenAIEmbeddingFunction(
                                api_key=openai_api_key,
                                model_name="text-embedding-3-small"
                            )
                self.embedding_model = embedding_model
            elif embedding_model == 'text-embedding-3-large':
                openai_api_key = input("Enter your OpenAI API key: ")
                self.ef = embedding_functions.OpenAIEmbeddingFunction(
                                api_key=openai_api_key,
                                model_name="text-embedding-3-large"
                            )
                self.embedding_model = embedding_model
            else:
                raise ValueError("Invalid embedding model.")
        elif db_path is None:
            self.use_chromdb = False    
        else:
            raise ValueError("Invalid arguments.")
        
    def parse_obo(self, obo_path):
        with open(obo_path, 'r') as f:
            lines = f.readlines()
        hpo_object_list = []
        hpo_object = {}
        id = ""
        name = ""
        synonyms = []
        defition = ""
        for line in lines:
            if line.startswith('[Term]'):
                if id != "":
                    hpo_object = {
                        'document': f"Term: {name}. Synonyms: {";".join(synonyms)}. Definition: {defition}",
                        'metadata': {
                            'term': name,
                            'synonyms': ";".join(synonyms)
                        },
                        'id': id
                    }
                    hpo_object_list.append(hpo_object)
                hpo_object = {}
                id = ""
                name = ""
                synonyms = []
                defition = ""
            elif line.startswith('id: HP:'):
                id = line.split(' ')[1].strip()
            elif line.startswith('name: '):
                name = line.split('name: ')[1].strip()
            elif line.startswith('synonym: '):
                synonyms.append(line.split('"')[1])
            elif line.startswith('def: '):
                defition = line.split('"')[1]
        return hpo_object_list
    
    def index_hpo(self):
        hpo_object_list = self.parse_obo(self.obo_path)
        
        if self.use_chromdb:
            if self.embedding_model is None:
                # create collection
                collection = self.chromadb_client.get_or_create_collection(name='hpo_default')
            else:
                collection = self.chromadb_client.get_or_create_collection(name=f'hpo_{self.embedding_model}', embedding_function=self.ef)

            # do batch insert for every 100 documents
            i = 0
            while i < len(hpo_object_list):
                current_batch = hpo_object_list[i:i+100] if i+100 < len(hpo_object_list) else hpo_object_list[i:]
                documents = [b['document'] for b in current_batch]
                metadatas = [b['metadata'] for b in current_batch]
                ids = [b['id'] for b in current_batch]
                collection.upsert(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                i += 100
                print(f"Indexed {i} documents.")
        else:
            print("Use Woosh")
            # Define the schema
            schema = Schema(id=ID(stored=True, unique=True), term=TEXT(stored=True), content=TEXT(stored=True))
            index_dir = self.whoosh_path
            # Create the index directory if it doesn't exist
            if not os.path.exists(index_dir):
                os.mkdir(index_dir)
                ix = index.create_in(index_dir, schema)  # Create the index in the directory
            else:
                ix = index.open_dir(index_dir)  # Open the existing index

            # Add documents to the index
            
            i = 0
            while i < len(hpo_object_list):
                writer = ix.writer()
                current_batch = hpo_object_list[i:i+100] if i+100 < len(hpo_object_list) else hpo_object_list[i:]
                documents = [b['document'] for b in current_batch]
                metadatas = [b['metadata'] for b in current_batch]
                for object in current_batch:
                    writer.add_document(id=object['id'], term=object['metadata']['term'], content=object['document'])
                writer.commit()
                i += 100
                print(f"Indexed {i} documents.")
                
            
    def query_hpo(self, text, n_results=1):
        
        if self.use_chromdb:
            if self.embedding_model is None:
                # get collection
                collection = self.chromadb_client.get_collection(name='hpo_default')
            else:
                collection = self.chromadb_client.get_collection(name=f'hpo_{self.embedding_model}', embedding_function=self.ef)
            # query
            results = collection.query(
                query_texts=[text],
                n_results=n_results, 
            )
            # a potential chromdb bug here. 
            # different results will be returned in different runs
            # due to Approximate Nearest Neighbors (ANN) search algorithm that Chroma uses. 
            # ANN algorithms are designed to prioritize speed over absolute accuracy, 
            # which means they may not always return the exact nearest neighbors, 
            # especially when the distances between the vectors are very close.
            # so n_results = 5 might be different from n_results = 25
            # https://github.com/chroma-core/chroma/issues/860
            return results
        else:
            ix = index.open_dir(self.whoosh_path)
            with ix.searcher() as searcher:
                # Get a collector object
                c1 = searcher.collector(limit=100, sortedby="term")
                # c2 = searcher.collector(limit=None, sortedby="content")
                # # Wrap it in a TimeLimitedCollector and set the time limit to 10 seconds
                tlc1 = TimeLimitCollector(c1, timelimit=5.0)
                # tlc2 = TimeLimitCollector(c1, timelimit=5.0)

                # Search in the title field
                term_query = QueryParser("term", ix.schema).parse(text)
                term_results = searcher.search(term_query)
                
                if term_results is not None and not term_results.is_empty():
                    results = term_results
                else:
                    content_query = QueryParser("content", ix.schema).parse(text)
                    results = searcher.search(content_query)
                    
                    if results is None or results.is_empty():
                        # query with 'OR' operator
                        terms = text.split()
                        query = " OR ".join(terms)
                        try:
                            content_query = QueryParser("term", ix.schema).parse(query)  
                            results = searcher.search_with_collector(content_query, tlc1)
                        except TimeLimit:
                            print("Time limit exceeded for content search.")
                            results = None
                if results is None or results.is_empty():
                    return (None, None)
                else:
                    number_of_results = min(n_results, len(results.top_n))                    
                    result_list = []
                    for i in range(number_of_results):
                        hpo_id = results[i]['id']
                        hpo_name = results[i]['term']
                        score = results[i].score
                        result_list.append((hpo_id, hpo_name, score))
                    return result_list
                    

    def parse_results(self, results, distance_threshold = 1.5):
        # if more than one results raise error
        if self.use_chromdb:
            if len(results['distances'][0]) > 1:
                raise ValueError("More than one results found.")
            if results['distances'][0][0] < distance_threshold:
                hpo_id = results['ids'][0][0]
                hpo_name = results['metadatas'][0][0]['term']
                return hpo_id, hpo_name
            else:
                return None, None
        else:
            if results[0] is None:
                return None, None
            else:
                return results[0][0], results[0][1]
            
    
    def parse_results_n_results(self, results):
        if self.use_chromdb:
            parsed_n_results = []
            for top_k in range(len(results['distances'][0])):
                hpo_id = results['ids'][0][top_k]
                hpo_name = results['metadatas'][0][top_k]['term']
                distance = results['distances'][0][top_k]
                parsed_n_results.append({'hpo_id': hpo_id, 'hpo_name': hpo_name, 'top_k': top_k, 'distance': distance})
            return parsed_n_results 
        else:
            parsed_n_results = []
            if results[0] is None:
                return parsed_n_results
            for top_k in range(len(results)):
                hpo_id = results[top_k][0]
                hpo_name = results[top_k][1]
                distance = -results[top_k][2]
                parsed_n_results.append({'hpo_id': hpo_id, 'hpo_name': hpo_name, 'top_k': top_k, 'distance': distance})
            return parsed_n_results
        
        
    
           
            

# Example usage
if __name__ == "__main__":
    db_path = 'hpo_chroma_db'
    obo_path = 'hp.obo'
    whoosh_path = 'hpo_whoosh_db'
    
    hpo_db = HpoDatabase(obo_path=obo_path, db_path=db_path, woosh_path=None, embedding_model='text-embedding-3-large')
    # chroma run --path ./hpo_chroma_db
    # hpo_object_list = hpo_db.parse_obo(obo_path)
    # print(hpo_object_list[:5])
    # hpo_db.index_hpo()
    # hpo_term = "Feeding difficulties"
    # results = hpo_db.query_hpo(hpo_term, n_results=1)
    # hpo_id, hpo_name = hpo_db.parse_results(results)
    # print(hpo_id, hpo_name)
    
    # hpo_term = "Fed difficulties"
    # results = hpo_db.query_hpo(hpo_term, n_results=1)
    # hpo_id, hpo_name = hpo_db.parse_results(results)
    # print(hpo_id, hpo_name)
    
    # hpo_term = "muscle difficulties"
    synonm = ["muscle weakness", "muscle pain", "muscle fatigue"]
    results = hpo_db.query_hpo(synonm, n_results=5)
    parsed_n_results = hpo_db.parse_results_n_results(results)
    print(parsed_n_results)
    
    # results = hpo_db.query_hpo(hpo_term, n_results=100, use_chromdb=False)
    # parsed_n_results = hpo_db.parse_results_n_results(results, use_chromdb=False)
    # print(parsed_n_results)
    
    
        
            
            
        


    
