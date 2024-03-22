import json
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key='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')

# Load the prompt from a file
with open('prompt.txt', 'r') as f:
    prompt = f.read()

# Load the documentation strings from a JSON file
with open('import_docs.json', 'r') as f:
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
