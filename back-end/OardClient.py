import requests

class OardClient:
    def __init__(self, base_url="https://rare.cohd.io/api/", api_key=None):
        """
        Initialize the OardClient.

        :param base_url: The base URL of the API to query.
        :param api_key: API key for authentication (if required).
        """
        self.base_url = base_url
        self.api_key = api_key

    def get_frequency(self, hpo_id, dataset_id=2, additional_params=None):
        """
        Get the frequency of an HPO ID in a dataset.

        :param hpo_id: The HPO ID to query.
        :param dataset: The dataset to search in.
        :param additional_params: Additional parameters for the API query (dict).
        :return: Frequency value or response from the API.
        """
        try:
            # Build the API endpoint URL
            endpoint = f"{self.base_url}/vocabulary/findConceptByCode"

            # Construct the query parameters
            params = {
                "q": hpo_id,
            }
            response = requests.get(endpoint, params=params)
            concept_ids = [response.json()['results'][i]["concept_id"] for i in range(len(response.json()['results'])) if response.json()['results'][i]["vocabulary_id"] == "hpo"]
            concept_id = concept_ids[0] if concept_ids != [] else None
            
            if concept_id is None:
                return None
        
            endpoint = f"{self.base_url}/frequencies/singleConceptFreq"
            
            # Construct the query parameters
            params = {
                "dataset_id": dataset_id,
                "concept_id": concept_id,
            }
            # Add additional parameters if provided
            if additional_params:
                params.update(additional_params)
            
            response = requests.get(endpoint, params=params)
            # Raise an error for unsuccessful responses
            frequency = response.json()['results'][0]['concept_frequency'] if response.json()['results'] != [] else None
            return frequency
        except Exception as e:
            raise ValueError("Failed to query the OARD API." + str(e)) from e
            
        
    
    def get_frequencies(self, hpo_ids, dataset_id=2, additional_params=None):
        """
        Get the frequency of an HPO ID in a dataset.

        :param hpo_id: The HPO ID to query.
        :param dataset: The dataset to search in.
        :param additional_params: Additional parameters for the API query (dict).
        :return: Frequency value or response from the API.
        """
        try:
            # Remove None from hpo_ids
            hpo_ids = [hpo_id for hpo_id in hpo_ids if hpo_id is not None]
            if hpo_ids == []:
                return None
            # Build the API endpoint URL
            endpoint = f"{self.base_url}/vocabulary/findConceptByCode"

            # Construct the query parameters
            params = {
                "q": ';'.join(hpo_ids),
            }
            response = requests.get(endpoint, params=params)
            concept_ids = [response.json()['results'][i]["concept_id"] for i in range(len(response.json()['results'])) if response.json()['results'][i]["vocabulary_id"] == "hpo"]
            if concept_ids == []:
                return None
        
            endpoint = f"{self.base_url}/frequencies/singleConceptFreq"
            
            # Construct the query parameters
            params = {
                "dataset_id": dataset_id,
                "concept_id": ';'.join([str(concept_id) for concept_id in concept_ids]),
            }
            # Add additional parameters if provided
            if additional_params:
                params.update(additional_params)
            
            response = requests.get(endpoint, params=params)
            # Raise an error for unsuccessful responses
            if response.json()['results'] == []:
                return None
            frequency = [{'hpo_id': response.json()['results'][i]['concept_code'], 'frequency': response.json()['results'][i]['concept_frequency']} for i in range(len(response.json()['results']))]
            frequecy_dict = {frequency[i]['hpo_id']: frequency[i]['frequency'] for i in range(len(frequency))}
            return frequecy_dict
        except Exception as e:
            raise ValueError("Failed to query the OARD API." + str(e)) from e

# Example usage:
if __name__ == "__main__":
    # Initialize the client
    client = OardClient()
    # Get the frequency of an HPO ID
    result = client.get_frequency(hpo_id="HP:0012361000")
    assert result is None
    result = client.get_frequency(hpo_id="HP:0003641")
    assert result == 0.00013705064058210223
    result = client.get_frequency(hpo_id="HP:0001945")
    assert result == 0.08858212592953671
    result = client.get_frequencies(hpo_ids=["HP:0003641", "HP:0001945"])
    print(result)