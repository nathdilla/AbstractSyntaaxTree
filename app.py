from flask import Flask, request, jsonify, redirect, render_template, session
from werkzeug.utils import secure_filename
import os
import javalang
import json
import requests
from bs4 import BeautifulSoup

# Setup Flask app
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'java'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload directory exists

global_roles_values = []
global_imports = []
global_types = []



# Check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# AST Generation Logic (from tree.py)
def generate_ast(java_file_path):
    with open(java_file_path, 'r') as file:
        java_code = file.read()
    try:
        tree = javalang.parse.parse(java_code)
        return tree
    except javalang.parser.JavaSyntaxError as e:
        print(f"Error parsing Java file: {e}")
        return None

def node_to_dict(node):
    node_dict = {'type': str(type(node).__name__)}
    for attr in node.attrs:
        value = getattr(node, attr)
        if isinstance(value, list):
            value = [node_to_dict(child) if isinstance(child, javalang.ast.Node) else str(child) for child in value]
        elif isinstance(value, javalang.ast.Node):
            value = node_to_dict(value)
        else:
            value = str(value)
        node_dict[attr] = value
    return node_dict

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

def extract_roles_values(node, roles_values, imports, types):
    """Recursively traverse the AST and extract roles, values, and types."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == 'path' and node.get('type') == 'Import':
                imports.append(value)
            elif key == 'name' and node.get('type') in ['ClassDeclaration', 'ReferenceType']:
                role = 'class' if node.get('type') == 'ClassDeclaration' else 'variable_type'
                roles_values.append({'role': role, 'value': value})
                types.append(node.get('type'))
            elif key == 'name' and node.get('type') == 'MethodDeclaration' and value is not None:  # Changed 'None' to None
                roles_values.append({'role': 'function', 'value': value})
            elif key == 'value' and node.get('type') == 'Literal' and value is not None:  # Changed 'None' to None
                roles_values.append({'role': 'literal', 'value': value})
            elif isinstance(value, (dict, list)):
                extract_roles_values(value, roles_values, imports, types)

    elif isinstance(node, list):
        for item in node:
            extract_roles_values(item, roles_values, imports, types)

def read_and_process_ast(ast_data):
    roles_values = []
    imports = []
    types = []
    extract_roles_values(ast_data, roles_values, imports, types)
    return roles_values, imports, types

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the uploaded file to generate AST
        ast = generate_ast(filepath)
        if ast:
            ast_dict = node_to_dict(ast)
            # Convert AST dict to formatted JSON string and store in session
            roles_values, imports, types = read_and_process_ast(ast_dict)

            session['roles_values'] = roles_values
            session['imports'] = imports
            session['types'] = types

            # Fetch documentation for imports and store in session
            import_docs = {}
            for import_node in imports:
                documentation = get_documentation_from_import(import_node)
                import_docs[import_node] = documentation
            session['import_docs'] = import_docs
            json_str = json.dumps(ast_dict, indent=4)
            # Render the HTML template with JSON data
            return render_template('result.html', json_data=json_str)
        else:
            return jsonify({'error': 'Failed to generate AST'})
    
    # HTML form for uploading files
    return '''
    <!doctype html>
    <title>Upload Java File</title>
    <h1>Upload a Java File for AST Generation</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/analysis')
def analysis():
    # Access the AST data from session
    roles_values = session.get('roles_values', [])
    imports = session.get('imports', [])
    types = session.get('types', [])
    import_docs = session.get('import_docs', {})

    #print the session data
    print("bruh")
    print(roles_values)
    print(imports)
    print(types)
    print(import_docs) 

    return render_template('analysis.html', roles_values=roles_values, imports=imports, types=types, import_docs=import_docs)

if __name__ == '__main__':
    app.run(debug=True)