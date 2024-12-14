import requests

class HpoLookup():
    def __init__(self):
        pass
        
        
    @staticmethod
    def search_hpo_in_ncbi(search_query):
        ncbi_url="https://clinicaltables.nlm.nih.gov/api/hpo/v3/search"
        '''
        Search HPO in NCBI database
        '''
        try:
            # Fetch data from the API
            response = requests.get(f"{ncbi_url}?terms={search_query}")
            response.raise_for_status()  # Raise an error for HTTP error codes
            data = response.json()

            # Reformat the data to match the expected format
            hpo_id_name_list = data[3]
            hpo_id_name_format_list = [{"id": hpo[0], "name": hpo[1]} for hpo in hpo_id_name_list]

            # Return the suggestions
            return hpo_id_name_format_list
        except requests.RequestException as e:
            print(f"Error fetching suggestions: {e}")
            return [] 
    
    @staticmethod
    def get_lowest_hpo(hpo_id_name_format_list, hpo_levels):
        print(hpo_id_name_format_list)
        # remove items not in hpo_levels
        hpo_id_name_format_list_in_hpo_levels = [hpo for hpo in hpo_id_name_format_list if hpo["id"] in hpo_levels]
        if len(hpo_id_name_format_list_in_hpo_levels) == 0:
            return [hpo_id_name_format_list[0]]
        
        if len(hpo_id_name_format_list_in_hpo_levels) == 1:
            return hpo_id_name_format_list
        
        # get the lowest level hpo id from hpo_id_name_format_list using hpo_levels
        lowest_hpo = [max(hpo_id_name_format_list_in_hpo_levels, key=lambda hpo: hpo_levels[hpo["id"]])]
        return lowest_hpo
    
    @staticmethod
    def add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels, gpt_response_hpo_terms=None, oard_client=None):
        '''
        Add HPO attributes to the matched intervals
        '''
        try:
            matched_hpo = []
            if gpt_response_hpo_terms:
                assert len(intervals) == len(gpt_response_hpo_terms), "Length of intervals and gpt_response_hpo_terms should be the same."
            
            for i in range(len(intervals)):
                start, end = intervals[i]
                selected_text = text[start:end]
                query = text[start:end]
                if query in hpo_dict:  
                    hpo_id = hpo_dict[query]
                    hpo_name = hpo_name_dict[hpo_id]
                else:
                    hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi(query)
                    if len(hpo_id_name_format_list) > 1:
                        hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
                    if len(hpo_id_name_format_list) > 0:
                        hpo_id = hpo_id_name_format_list[0]["id"]
                        hpo_name = hpo_id_name_format_list[0]["name"]   
                    else:
                        hpo_id = None
                        hpo_name = None
                
                if hpo_id is None:
                    # use GPT term as back up
                    query = gpt_response_hpo_terms[i]
                    if query in hpo_dict:  
                        hpo_id = hpo_dict[query]
                        hpo_name = hpo_name_dict[hpo_id]
                    else:
                        hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi(query)
                        if len(hpo_id_name_format_list) > 1:
                            hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
                        if len(hpo_id_name_format_list) > 0:
                            hpo_id = hpo_id_name_format_list[0]["id"]
                            hpo_name = hpo_id_name_format_list[0]["name"]
                            
                        else:
                            hpo_id = None
                            hpo_name = None
                matched_hpo.append((start, end, selected_text, {"id": hpo_id, "name": hpo_name}))
            return matched_hpo
        except Exception as e:
            raise ValueError("Failed to add HPO attributes to the matched intervals." + str(e))
        
    @staticmethod
    def add_hpo_frequency(matched_hpo, oard_client):
        frequency_dict = oard_client.get_frequencies([hpo[3]["id"] for hpo in matched_hpo])
        print(frequency_dict)
        if frequency_dict is None:
            return matched_hpo
        for hpo in matched_hpo:
            hpo[3]["frequency"] = frequency_dict[hpo[3]["id"]] if hpo[3]["id"] in frequency_dict else None
        return matched_hpo
    

    
            
        
        
# Example usage
if __name__ == "__main__":
    from HpoFactory import HpoFactory
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    print(hpo_levels)
    hpo_dict, hpo_name_dict, _ = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi("abnormal gait")
    print(hpo_id_name_format_list)
    hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
    print(hpo_id_name_format_list)
    
    matched_hpo = HpoLookup.add_hpo_attributes("abnormal gait", [(0, 12)], hpo_dict, hpo_name_dict, hpo_levels)
    print(matched_hpo)
    from OardClient import OardClient
    oard_client = OardClient()
    matched_hpo = HpoLookup.add_hpo_attributes("fever", [(0, 5)], hpo_dict, hpo_name_dict, hpo_levels)
    matched_hpo = HpoLookup.add_hpo_frequency(matched_hpo, oard_client)
    print(matched_hpo)