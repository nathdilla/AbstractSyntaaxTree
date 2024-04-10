from tree import JavaASTGenerator

ast_generator = JavaASTGenerator("java/TaskManager.java")
ast_generator.generate_ast_json('outputs/AST.json')