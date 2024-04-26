import psycopg2
from psycopg2.extras import Json
import json

class PopulateDB:
    def __init__(self, outputfile):
        self.outputfile = outputfile

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                dbname='pgPrinciples', 
                user='postgres', 
                password='Qazssedc9', 
                host='localhost',
                port='5433'
            )
            return conn
        except psycopg2.Error as e:
            print("Error: Unable to connect to the database.")
            print(e)
            exit()

    def load_json(self,file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def insert_json_data(self,cur, json_data, table, columns):
        for key, value in json_data.items():
            cur.execute(
                f"INSERT INTO public.{table} ({', '.join(columns)}) VALUES (%s, %s)", 
                (key, value)
            )
            print(f"Inserted {key} into the {table} table")

    def populate(self):
        conn = self.connect_db()
        cur = conn.cursor()
        
        domain_data = self.load_json(self.outputfile + '/ClassDomains.json')
        self.insert_json_data(cur, domain_data, "class_domains", ["import", "type"])

        ast_data = self.load_json(self.outputfile + '/AST.json')
        cur.execute("INSERT INTO public.ast (ast_data) VALUES (%s)", [Json(ast_data)])
        print("Inserted into the AST table")

        summary_data = self.load_json(self.outputfile + '/ClassSummary.json')
        self.insert_json_data(cur, summary_data, "class_summary", ["class_name", "description"])

        documentation_data = self.load_json(self.outputfile + '/Documentation.json')
        self.insert_json_data(cur, documentation_data, "documentation", ["import", "documentation"])

        func_domain_data = self.load_json(self.outputfile + '/FunctionDomains.json')
        self.insert_json_data(cur, func_domain_data, "function_domain", ["function_", "domain_"])

        function_data = self.load_json(self.outputfile + '/Functions.json')
        for key, info in function_data.items():
            if info is not None:
                cur.execute(
                    "INSERT INTO public.functions (key, class_name, function_name, description) VALUES (%s, %s, %s, %s)",
                    (key, info['class'], info['function'], info['description'])
                )
            else:
                print(f"Warning: No data for key {key}")

        similarity_data = self.load_json(self.outputfile + '/Similarities.json')
        for class_name, tests in similarity_data.items():
            for test_name, category in tests.items():
                cur.execute(
                    "INSERT INTO similarities (class_name, test_name, category) VALUES (%s, %s, %s)",
                    (class_name, test_name, category)
                )    
                print(f"Inserted {test_name} into the similarities table")

        conn.commit()
        cur.close()
        conn.close()
