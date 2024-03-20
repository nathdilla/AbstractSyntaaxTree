import json

def extract_roles_values(node, roles_values, imports, types):
    """Recursively traverse the AST and extract roles, values, and types."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'path' and node.get('type') == '<class \'javalang.tree.Import\'>':
                imports.append(value)
            elif key == 'name' and node.get('type') in ['<class \'javalang.tree.ClassDeclaration\'>', '<class \'javalang.tree.ReferenceType\'>']:
                role = 'class' if node.get('type') == '<class \'javalang.tree.ClassDeclaration\'>' else 'variable_type'
                roles_values.append({'role': role, 'value': value})
                types.append(node.get('type'))
            elif key == 'name' and node.get('type') == '<class \'javalang.tree.MethodDeclaration\'>' and value != 'None':
                roles_values.append({'role': 'function', 'value': value})
            elif key == 'value' and node.get('type') == '<class \'javalang.tree.Literal\'>' and value != 'None':
                roles_values.append({'role': 'literal', 'value': value})
            elif isinstance(value, (dict, list)):
                extract_roles_values(value, roles_values, imports, types)

    elif isinstance(node, list):
        for item in node:
            extract_roles_values(item, roles_values, imports, types)

def read_and_process_ast(filepath):
    """Read AST from file and process to identify roles, values, and types."""
    try:
        with open(filepath, 'r') as file:
            ast_data = json.load(file)

        roles_values = []
        imports = []
        types = []
        extract_roles_values(ast_data, roles_values, imports, types)
        return roles_values, imports, types
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return [], [], []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {filepath}")
        return [], [], []


import requests
from bs4 import BeautifulSoup

def get_documentation_from_import(import_statement):
    """
    Fetches and prints the overview summary for a given Java class based on its import statement.

    :param import_statement: Import statement of the Java class, e.g., 'java.util.Scanner'.
    :return: Overview summary text or an error message.
    """
    # Base URL for Java SE 10 documentation. Adjust as necessary for different Java versions.
    base_url = 'https://docs.oracle.com/javase/10/docs/api/'
    
    # Construct the URL from the import statement
    path = import_statement.replace('.', '/') + '.html'
    url = base_url + path

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Adjust the find parameters based on the actual HTML structure.
            # For demonstration, let's attempt to find and return the class description.
            # This is a simplified example and might need adjustments.
            description = soup.find('div', class_='description')
            if description:
                return description.text.strip()
            else:
                return "Class description not found."
        else:
            return "Failed to retrieve the documentation due to a network error."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# # Example usage
# if __name__ == "__main__":
#     filepath = 'output.json'
#     roles_values, imports, types = read_and_process_ast(filepath)
    
#     with open('documentation.txt', 'w') as f:  # Open documentation.txt in write mode
#         f.write("Roles and Values:\n")
#         f.write(str(roles_values))
#         f.write("\n\nImports:\n")
#         f.write(str(imports))
#         f.write("\n\nTypes:\n")
#         f.write(str(types))
#         f.write("\n\n")

#         for import_node in imports:
#             documentation = get_documentation_from_import(import_node)
#             f.write(documentation + '\n')  # Write the documentation to the file

import json

# Example usage
if __name__ == "__main__":
    filepath = 'output.json'
    roles_values, imports, types = read_and_process_ast(filepath)
    
    import_docs = {}
    for import_node in imports:
        documentation = get_documentation_from_import(import_node)
        import_docs[import_node] = documentation  # Store the documentation in a dictionary

    with open('import_docs.json', 'w') as f:  # Open import_docs.json in write mode
        json.dump(import_docs, f, indent=4)  # Write the import documentation dictionary to the file as JSON

    