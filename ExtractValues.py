import json
import requests
from bs4 import BeautifulSoup

class ExtractValues:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_roles_values(self, node, roles, imports, types, variables):
        """Recursively traverse the AST and extract roles, values, and types."""
        if isinstance(node, dict):
            for key, value in node.items():
                if key == 'path' and node.get('type') == '<class \'javalang.tree.Import\'>':
                    imports[value.split('.')[-1]] = value
                elif key == 'name' and node.get('type') == '<class \'javalang.tree.ClassDeclaration\'>':
                    roles['class'].append({'role': 'class', 'value': value})
                    types[value] = node  # Storing node as type information
                elif key == 'name' and node.get('type') == '<class \'javalang.tree.VariableDeclarator\'>':
                    initializer = node.get('initializer', {})
                    if isinstance(initializer, dict):
                        type_info = initializer.get('type', {})
                        if isinstance(type_info, dict):
                            class_type = type_info.get('name')
                            if class_type:
                                variables[value] = class_type
                elif key == 'member' and node.get('type') == '<class \'javalang.tree.MethodInvocation\'>':
                    qualifier = node.get('qualifier')
                    if qualifier in variables:
                        qualifier = variables[qualifier]
                    if qualifier in imports:
                        qualifier = imports[qualifier]
                    roles['function'].append({'class': qualifier, 'function': value})
                elif isinstance(value, (dict, list)):
                    self.extract_roles_values(value, roles, imports, types, variables)
                if node.get('type') == '<class \'javalang.tree.Literal\'>' and key == 'value':
                    roles['literal'].append({'role': 'literal', 'value': value})

        elif isinstance(node, list):
            for item in node:
                self.extract_roles_values(item, roles, imports, types, variables)

    def read_and_process_ast(self):
        """Read AST from file and process to identify roles, values, and types."""
        try:
            with open(self.filepath, 'r') as file:
                ast_data = json.load(file)

            roles = {'class': [], 'function': [], 'literal': []}
            imports = {}
            types = {}
            variables = {}
            self.extract_roles_values(ast_data, roles, imports, types, variables)
            return roles, imports, types
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            return [], [], []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file: {self.filepath}")
            return [], [], []

    @staticmethod
    def remove_duplicates(lst):
        """Remove duplicate entries from a list."""
        return [dict(t) for t in {tuple(d.items()) for d in lst}]

    def filter_functions_by_imports(self, functions, imports):
        """Filter out function entries where the class is not in imports."""
        return [func for func in functions if func['class'] in imports.values()]

    def extract(self, OUTPUT_DIR):
        try:
            roles_values, imports, types = self.read_and_process_ast()
            roles_values['function'] = self.remove_duplicates(roles_values['function'])
            roles_values['function'] = self.filter_functions_by_imports(roles_values['function'], imports)
            print("Roles and Values:")
            for role, values in roles_values.items():
                print(f"\n{role.capitalize()}s:")
                for value in values:
                    print(value)
                print("Error: roles_values is a list, not a dictionary.")
            print("\nImports:")
            print(imports)

            import_docs = {}
            for imported, importStatement in imports.items():
                documentation = self.get_documentation_from_import(importStatement)
                import_docs[imported] = documentation

            with open(OUTPUT_DIR+'/Documentation.json', 'w') as f:
                json.dump(import_docs, f, indent=4)

            print("\Imported Functions:")
            functions = {}
            for value in roles_values['function']:
                classToSearch = value['class']
                function = value['function']
                # print(f"\nClass: {classToSearch}, Function: {function}")
                result = self.summarize_function(classToSearch, function)
                #add result to functions dictionary
                functions[classToSearch + '.' + function] = result
                print(result)
            with open(OUTPUT_DIR+'/Functions.json', 'w') as f:
                json.dump(functions, f, indent=4)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        with open(OUTPUT_DIR+'/Functions.json', 'w') as f:
                json.dump("functions", f, indent=4)
        

    @staticmethod
    def get_documentation_from_import(import_statement):
        """Fetch Java SE documentation for a given import."""
        base_url = 'https://docs.oracle.com/javase/10/docs/api/'
        path = import_statement.replace('.', '/') + '.html'
        url = base_url + path
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                description = soup.find('div', class_='description')
                if description:
                    return description.text.strip()
                else:
                    return "Class description not found."
            else:
                return "Failed to retrieve the documentation due to a network error."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @staticmethod
    def summarize_function(classToSearch, function):
        """Summarize function details from Java documentation."""
        base_url = 'https://docs.oracle.com/javase/10/docs/api/'
        path = classToSearch.replace('.', '/') + '.html'
        url = base_url + path
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                h4_tag = soup.find('h4', string=function)
                if h4_tag:
                    block_div = h4_tag.find_next_sibling('div', class_='block')
                    if block_div:
                        # print("Description of the function:")
                        # print(block_div.text.strip())
                        return {'class': classToSearch, 'function': function, 'description': block_div.text.strip()}
                    else:
                        print("No 'div' with class 'block' found after the specified 'h4' tag.")
                else:
                    print("Function not found in the documentation.")
            else:
                return "Failed to retrieve the documentation due to a network error."
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
        
