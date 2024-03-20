import sys
import javalang
import json

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
    node_dict = {'type': str(type(node))}
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

if __name__ == "__main__":
    java_file_path = "TaskManager.java"  # Hardcoded filename
    ast = generate_ast(java_file_path)

    if ast:
        ast_dict = node_to_dict(ast)
        with open('output.json', 'w') as f:  # Open output.json in write mode
            json.dump(ast_dict, f, indent=4)  # Write the AST dictionary to the file as JSON