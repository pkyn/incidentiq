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

api_url = os.getenv("API_URL")
if not api_url:
    raise ValueError("API URL not found. Please set the API_URL environment variable.")

bearer_token = os.getenv("API_TOKEN")
if not bearer_token:
    raise ValueError("Bearer token not found. Please set the API_TOKEN environment variable.")

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
    # prompt = "your are an expert in analyzing the data and extracting fields from a jason object. for the given json data "+ json.dumps(data) +" extract test dimension, syntheticMetrics and syntheticMetrics values from detail and format it into a CSV structure"
    #metrics, dimensions id and name where id is 16 from responseItems then dimensions id and name where id is 16 or 1 and values from items. include only Test Time (ms), % Ping Packet Loss, % Availability,"
    #"Jitter, Time to Leave metrics in the result and result should be formatted to a csv file which contains only items

    prompt = "your are an expert in analyzing the data and extracting fields from a jason. you have the given json data: "+ json.dumps(data) +" extract dimensions id and name where id is 16 and 1 and metrics array and also values from items. metrics array has the metric name and values arrays has metric value The index from metric array will match position in values array. Include only following metrics in the result: Test Time (ms), % Availability, % Ping Packet Loss, Jitter (ms), Ping Round Trip (ms)"
    client = genai.Client(api_key=os.getenv("SECRET_KEY"))
    # Generate content using the model
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents='high',
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                #max_output_tokens=1024,
                temperature=0.3,
            )
        )

        print(response.text)

        response2 = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents='high',
            config=types.GenerateContentConfig(
                system_instruction="extract distinct "+ json.dumps(response.text) +" into a CSV structure",
                #max_output_tokens=1024,
                temperature=0.3,
            )
        )

        csv_file = "summarized_data.csv"
        jsonl_file = "summarized_data_json.jsonl"

        with open(csv_file, 'w') as f:
            #   f.write(response.text + "\n")    
              f.write(response2.text + "\n")         
        with open(jsonl_file, 'w') as f:
              f.write(response.text + "\n")

        print(f"Data has been fetched, summarized, and saved to {csv_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

train_ai_model(data)