from openai import OpenAI
import typing_extensions as typing
import ast
from pydantic import BaseModel

class Terms(BaseModel):
    results: list[str]

class OpenaiApi:
    def __init__(self, model="gpt-4o-mini-2024-07-18",openai_api_key=None):
        if openai_api_key is None:
            user_input = input("Enter your OpenAI API key: ")
            if len(user_input) > 0:
                self.openai_api_key = user_input
            else:
                raise ValueError("OpenAI API key is required.")
        else:
            self.openai_api_key = openai_api_key
        
        self.model = model
            
            
    def run(self, prompt):
        try:
            client = OpenAI(api_key=self.openai_api_key)
            system_message="You are a helpful assistant."
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content":  system_message},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens = 1024,
                temperature = 0.8,
            )
            
            # Extract the terms and positions from the OpenAI response
            response = completion.choices[0].message.content
            return response
        except Exception as e:
            raise ValueError(f"Failed to query OpenAI {self.model}.\n Check your OpenAI Key. \n" + str(e))   
        
    def run_with_json(self, prompt, response_schema=Terms):
        try:
            system_message="You are a helpful assistant."
            client = OpenAI(api_key=self.openai_api_key)
            completion = client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content":  system_message},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens = 1024,
                temperature = 0.8,
                response_format=response_schema
            )
            
            # Extract the terms and positions from the OpenAI response
            response = completion.choices[0].message.parsed
            results_list = response.model_dump()["results"]
            return results_list
        except Exception as e:
            raise ValueError(f"Failed to query OpenAI {self.model}.\n Check your OpenAI Key. \n" + str(e))  
        
    
# Example usage
if __name__ == "__main__":
    api = OpenaiApi()
    user_message = "Generate 5 synonyms for the following term 'Muscle weakness' not including 'fatigue/weakness/atrophy/paralysis'. Return a json response."
    # response = api.run_openai(user_message)
    response = api.run_with_json(user_message)
    print(response)
    
    
    
    