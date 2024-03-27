import json
import os
from openai import OpenAI
from dotenv import load_dotenv # for loading environment variable

load_dotenv()

key = os.getenv('OPENAI_SECRET_KEY')
# Initialize the OpenAI client with your API key
client = OpenAI(api_key=key)

# Load the prompt from a file
with open('prompt.txt', 'r') as f:
    prompt = f.read()

# Load the documentation strings from a JSON file
with open('outputs/import_docs.json', 'r') as f:
    import_docs = json.load(f)

command = "Given the description, output the corresponding label. Just give me the label, nothing else."

# Iterate over each key and documentation string in the import_docs dictionary
for key, doc_string in import_docs.items():
    # Construct the request string with the current documentation string
    request = prompt + doc_string + command
    MODEL = "gpt-3.5-turbo"
    
    # Perform the API request
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": request},
        ],
        temperature=0,
    )

    # Concatenate the key with the response content
    result = f"{key}: {response.choices[0].message.content.strip()}"

    # Print the combined result
    print(result)
