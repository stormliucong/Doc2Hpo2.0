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


# Define the HPO database class
class HpoDatabase:
    def __init__(self, db_path, obo_path):
        
        self.chromadb_client = chromadb.PersistentClient(path=db_path)
        self.obo_path = obo_path
        
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
        
        # create collection
        collection = self.chromadb_client.get_or_create_collection(name='hpo_default')
        
        hpo_object_list = self.parse_obo(self.obo_path)
        # do batch insert for every 100 documents
        i = 0
        while i < len(hpo_object_list):
            current_batch = hpo_object_list[i:i+100] if i+100 < len(hpo_object_list) else hpo_object_list[i:]
            documents = [b['document'] for b in current_batch]
            metadatas = [b['metadata'] for b in current_batch]
            ids = [b['id'] for b in current_batch]
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            i += 100
            print(f"Indexed {i} documents.")
            

# Example usage
if __name__ == "__main__":
    db_path = 'hpo_chroma_db'
    obo_path = 'hp.obo'
    
    hpo_db = HpoDatabase(db_path, obo_path)
    # chroma run --path ./hpo_chroma_db
    # hpo_object_list = hpo_db.parse_obo(obo_path)
    # print(hpo_object_list[:5])
    hpo_db.index_hpo()
        
            
            
        


    
