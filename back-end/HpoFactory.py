from collections import deque, defaultdict 
import os
import json

class HpoFactory:
    def __init__(self):
        # check if hpo.json exists
        if not os.path.exists("hp.obo"):
            # if not, build hpo.json
            raise FileNotFoundError("hp.obo not found. please download it from https://hpo.jax.org/data/ontology and put it under root flask folder.")
        self.hpo_file = "hp.obo"
    
    def build_hpo_tree(self):
        hpo_tree = defaultdict(list)
        with open(self.hpo_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("id: "):
                    current_id = line.split("id: ")[1]
                elif line.startswith("is_a: ") and current_id:
                    parent_id = line.split("is_a: ")[1].split(" ! ")[0]
                    hpo_tree[current_id].append(parent_id)
        return hpo_tree
    
    def get_hpo_ancestors(self, hpo_tree):
        hpo_ancestors = defaultdict(list)
        for hpo_id in hpo_tree:
            queue = deque([hpo_id])
            while queue:
                current_id = queue.popleft()
                if current_id in hpo_tree:
                    for parent_id in hpo_tree[current_id]:
                        hpo_ancestors[hpo_id].append(parent_id)
                        queue.append(parent_id)
        return hpo_ancestors
    
    def build_hpo_dict(self, hpo_ancestors):
        hpo_dict = {}
        current_id = None
        with open(self.hpo_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("id: "):
                    current_id = line.split("id: ")[1]
                    # skip obsolete terms and id not under 'HP:0000118' in the hierarchy
                    if current_id not in hpo_ancestors or 'HP:0000118' not in hpo_ancestors[current_id]:
                        current_id = None
                        continue

                elif line.startswith("name: ") and current_id:
                    current_name = line.split("name: ")[1]
                    if current_name not in hpo_dict:
                        hpo_dict[current_name] = current_id
                        
                elif line.startswith("synonym: ") and current_id:
                    synonym = line.split("synonym: ")[1].split(" EXACT")[0].strip('"')  # Extract synonym text
                    if synonym not in hpo_dict:
                        hpo_dict[synonym] = current_id

                # Reset current_id and current_name when reaching a new stanza
                elif line == "[Term]" or line == "[Typedef]":
                    current_id = None
        return hpo_dict
    
    def expand_hpo_dict(self, hpo_dict):
        '''
        for each key in hpo_dict, add a new key by remove capitalization. But don't lower acronyms.
        '''
        expanded_hpo_dict = {}
        for k, v in hpo_dict.items():
            expanded_hpo_dict[k] = v
            # tokenize the key
            tokens = k.split()
            # don't lower acronyms
            tokens = [token.lower() if not token.isupper() else token for token in tokens]
            # remove special characters
            tokens = [token.strip('(),') for token in tokens]
            new_key = ' '.join(tokens)
            if new_key != '':
                expanded_hpo_dict[new_key] = v
        return expanded_hpo_dict
            
            

# Example usage
if __name__ == "__main__":
    hpoF = HpoFactory()
    hpo_tree = hpoF.build_hpo_tree()
    hpo_ancestors = hpoF.get_hpo_ancestors(hpo_tree)
    hpo_dict = hpoF.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpoF.expand_hpo_dict(hpo_dict)
    print(hpo_tree["HP:0000011"])
    print(hpo_ancestors["HP:0000011"])        
    assert hpo_dict['Lack of bladder control due to nervous system injury'] == 'HP:0000011'
    assert 'Autosomal dominant inheritance' not in hpo_dict
    assert 'HP:0000057' not in hpo_ancestors
    assert 'orofacial cleft' in hpo_dict
    assert '' not in hpo_dict
    assert 'abnormal' not in hpo_dict

