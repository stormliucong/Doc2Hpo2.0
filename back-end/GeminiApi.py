import google.generativeai as genai
import typing_extensions as typing
import ast

class GeminiApi:
    def __init__(self, api_key=None, model_id="gemini-1.5-flash-002"):
        if api_key is None:
            api_key = input("Enter your Gemini API key: ")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_id)
            
            
    def run(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
        
    def run_with_json(self, prompt, response_schema=list[str]):
        response = self.model.generate_content(prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=response_schema))
        string_list = response.text
        list_string = ast.literal_eval(string_list)
        assert isinstance(list_string, list) and all(isinstance(item, str) for item in list_string), "The response should be a list of strings."
        return list_string
    
# Example usage
if __name__ == "__main__":
    api = GeminiApi()
    # prompt = "List a few popular cookie recipes."
    # response = api.run_gemini(prompt)
    # print(response)
    
    # prompt = """List a few popular cookie recipes in JSON format.

    # Use this JSON schema:

    # Recipe = {'recipe_name': str, 'ingredients': list[str]}
    # Return: list[Recipe]"""
    # response = api.run_gemini_json(prompt, response_schema=list[str])
    # print(response)
    
    prompt = "Get 5 synonyms for the following terms 'Muscle weakness/fatigue/weakness/atrophy/paralysis'"
    response = api.run_gemini_json(prompt, response_schema=list[str])
    print(response)