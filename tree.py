import sys
import javalang
import json

class JavaASTGenerator:
    def __init__(self, java_file_path):
        self.java_file_path = java_file_path

    def generate_ast(self):
        with open(self.java_file_path, 'r') as file:
            java_code = file.read()

        try:
            tree = javalang.parse.parse(java_code)
            return tree
        except javalang.parser.JavaSyntaxError as e:
            print(f"Error parsing Java file: {e}")
            return None

    def node_to_dict(self, node):
        node_dict = {'type': str(type(node))}
        for attr in node.attrs:
            value = getattr(node, attr)
            if isinstance(value, list):
                value = [self.node_to_dict(child) if isinstance(child, javalang.ast.Node) else str(child) for child in value]
            elif isinstance(value, javalang.ast.Node):
                value = self.node_to_dict(value)
            else:
                value = str(value)
            node_dict[attr] = value
        return node_dict

    def generate_ast_json(self, output_file_path):
        ast = self.generate_ast()

        if ast:
            ast_dict = self.node_to_dict(ast)
            with open(output_file_path, 'w') as f:  # Open output.json in write mode
                json.dump(ast_dict, f, indent=4)  # Write the AST dictionary to the file as JSON