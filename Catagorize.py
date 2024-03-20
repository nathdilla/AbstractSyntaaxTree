import json
from openai import OpenAI

client = OpenAI(api_key='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')

command = "Given the description, output the corresponding label. Just give me the label, nothing else."
request = ""

with open('prompt.txt', 'r') as f:
    prompt = f.read()

with open('import_docs.json', 'r') as f:
    import_docs = json.load(f)

doc_strings = []
for import_node, documentation in import_docs.items():
    doc_strings.append(documentation)

# Now, doc_strings is a list of all documentations as strings.
for doc_string in doc_strings:
    request = prompt + doc_string + command
    MODEL = "gpt-3.5-turbo"
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": request},
    ],
    temperature=0,
    )

    print(response.choices[0].message.content)
    request = ""



