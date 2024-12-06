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
        # get the lowest level hpo id from hpo_id_name_format_list using hpo_levels
        lowest_hpo = max(hpo_id_name_format_list, key=lambda hpo: hpo_levels[hpo["id"]])
        return lowest_hpo
    
    @staticmethod
    def add_hpo_attributes(text, intervals, hpo_dict, hpo_name_dict, hpo_levels):
        '''
        Add HPO attributes to the matched intervals
        '''
        matched_hpo = []    
        for start, end in intervals:
            if text[start:end] in hpo_dict:
                hpo_id = hpo_dict[text[start:end]]
                hpo_name = hpo_name_dict[hpo_id]
            else:
                hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi(text[start:end])
                if len(hpo_id_name_format_list) > 1:
                    hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
                if hpo_id_name_format_list:
                    hpo_id = hpo_id_name_format_list["id"]
                    hpo_name = hpo_id_name_format_list["name"]
                else:
                    hpo_id = None
                    hpo_name = None
            matched_hpo.append((start, end, text[start:end], {"id": hpo_id, "name": hpo_name}))
        return matched_hpo
            
        
        
# Example usage
if __name__ == "__main__":
    from HpoFactory import HpoFactory
    hpo_F = HpoFactory()
    hpo_tree = hpo_F.build_hpo_tree()
    hpo_ancestors = hpo_F.get_hpo_ancestors(hpo_tree)
    hpo_levels = hpo_F.get_hpo_levels(hpo_tree)
    hpo_dict, hpo_name_dict = hpo_F.build_hpo_dict(hpo_ancestors)
    hpo_dict = hpo_F.expand_hpo_dict(hpo_dict)
    hpo_id_name_format_list = HpoLookup.search_hpo_in_ncbi("abnormal gait")
    print(hpo_id_name_format_list)
    hpo_id_name_format_list = HpoLookup.get_lowest_hpo(hpo_id_name_format_list, hpo_levels)
    print(hpo_id_name_format_list)
    matched_hpo = HpoLookup.add_hpo_attributes("abnormal gait", [(0, 12)], hpo_dict, hpo_name_dict, hpo_levels)
    print(matched_hpo)