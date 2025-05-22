import requests
import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import typing

# Step 1: Fetch the Data

# Load environment variables from .env file
load_dotenv()
key = os.getenv("SECRET_KEY")
if not key:
    raise ValueError("API key not found. Please set the SECRET_KEY environment variable.")

api_url = "https://ioqa.catchpoint.com/api/v4/tests/explorer/favoritechart/data/154325?pageNumber=1&pageSize=100"
bearer_token = "72F3A8D7F05CABC27562AC315CFFDDB75D1D7482E1EB9843E6D45D113ED0C7BD"

headers = {
"Authorization": f"Bearer {bearer_token}",
"Accept": "application/json",
"cp-api-preview": "true"
}
try:
    response = requests.get(api_url,headers=headers)
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching data: {e}")
    data = None
# train ai

def train_ai_model(data):
    # Initialize the Generative AI model
    prompt = "your are am expert in analyzing the data and extracting fields from a jason object. for the given json data "+ json.dumps(data) +" extract syntheticMetrics and syntheticMetrics values from detail and store in a csv file" 
    client = genai.Client(api_key=os.getenv("SECRET_KEY"))
    # Generate content using the model
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents='high',
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                max_output_tokens=1024,
                temperature=0.3,
            )
        )    
        jsonl_file = "summarized_data.json"

        with open(jsonl_file, 'w') as f:
              f.write(response.text + "\n")             
        print(f"Data has been fetched, summarized, and saved to {jsonl_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

train_ai_model(data)