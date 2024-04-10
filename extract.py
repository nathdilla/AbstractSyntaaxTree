import json
from collections import defaultdict
from openai import OpenAI


client = OpenAI(api_key='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')


def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def find_method_invocations(node, imported_classes, methods):
    if isinstance(node, dict):
        node_type = node.get('type')
        if node_type == "<class 'javalang.tree.MethodInvocation'>":
            qualifier = node.get('qualifier')
            method_name = node.get('member')
            # Check if the qualifier matches any of the imported classes.
            if qualifier and any(qualifier == class_name.split('.')[-1] for class_name in imported_classes):
                full_class_name = next((class_name for class_name in imported_classes if class_name.endswith(qualifier)), None)
                if full_class_name:
                    methods[full_class_name].append(method_name)
                    # Process selectors for nested method invocations within the valid scope
                    selectors = node.get('selectors', [])
                    if isinstance(selectors, list):
                        for selector in selectors:
                            if isinstance(selector, dict) and selector.get('type') == "<class 'javalang.tree.MethodInvocation'>":
                                nested_method_name = selector.get('member')
                                if nested_method_name:  # Only append if nested_method_name is defined
                                    methods[full_class_name].append(nested_method_name)

                                    MODEL = "gpt-3.5-turbo"

                                    response = client.chat.completions.create(
                                    model=MODEL,
                                    messages=[
                                        {"role": "user", "content": "describe" + nested_method_name + "in one sentence"},
                                    ],
                                    temperature=0,
                                    )
                                    # Concatenate the key with the response content
                                    result = f"{response.choices[0].message.content.strip()}"
                                    # Print the combined result
                                    print(result)

        # Recursively search child nodes
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                find_method_invocations(value, imported_classes, methods)

    elif isinstance(node, list):
        for item in node:
            find_method_invocations(item, imported_classes, methods)

def main(docs_path, ast_path):
    docs = load_json(docs_path)
    ast = load_json(ast_path)
    
    imported_classes = {import_stmt["path"] for import_stmt in ast.get("imports", [])}
    methods = defaultdict(list)
    find_method_invocations(ast, imported_classes, methods)
    
    for class_name, methods_list in methods.items():
        print(f"Imported Class: {class_name}, Methods: {', '.join(set(methods_list))}")

if __name__ == "__main__":
    docs_path = 'outputs/import_docs.json'
    ast_path = 'outputs/AST.json'
    main(docs_path, ast_path)
