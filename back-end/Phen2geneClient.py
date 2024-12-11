import requests

class Phen2geneClient:
    """
    Client for the Phen2Gene API.
    """
    def __init__(self, base_url="https://phen2gene.wglab.org/api"):
        """
        Initialize the client with the base URL of the API.
        
        :param base_url: The base URL of the API.
        """
        self.base_url = base_url
        
    def test_connection(self):
        """
        Test the connection to the API.
        
        :return: True if the connection is successful, False otherwise.
        """
        endpoint = f"{self.base_url}"
        response = requests.get(endpoint)
        return response.status_code == 200
    
    def get_genes(self, hpo_ids, additional_params=None):
        """
        Get the gene associated with an HPO ID.
        
        :param hpo_id: The HPO ID to query.
        :param additional_params: Additional parameters for the API query (dict).
        :return: Gene symbol or response from the API.
        """
        # Build the API endpoint URL
        endpoint = f"{self.base_url}"
        
        # Construct the query parameters
        params = {
            "HPO_list": ';'.join(hpo_ids),
        }
        # Add additional parameters if provided
        if additional_params:
            params.update(additional_params)
        
        response = requests.get(endpoint, params=params)
        # Raise an error for unsuccessful responses
        genes = response.json()['results'] if response.json()['results'] != [] else None
        return genes
    
    def filter_results(self, genes, rank=5, score=0.5, status=None):
        """
        Filter the results based on a threshold.
        
        :param results: The results to filter.
        :param threshold: The threshold value.
        :return: Filtered results.
        """
        if status is None:
            filtered_genes = [g for g in genes if int(g["Rank"]) <= rank and float(g["Score"]) >= score]
        else:
            filtered_genes = [g for g in genes if int(g["Rank"]) <= rank and float(g["Score"]) >= score and g["Status"] == status]
        return filtered_genes
    
# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = Phen2geneClient()
    
    # Test the connection
    print(client.test_connection())
    
    # Get the gene for an HPO ID
    hpo_id = ["HP:0002459", "HP:0001662"]
    genes = client.get_genes(hpo_id)
    filtered_genes = client.filter_results(genes)
    print(filtered_genes)
    