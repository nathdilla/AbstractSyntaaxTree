import psycopg2
from psycopg2.extras import Json
import json

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname='pgPrinciples', 
            user='postgres', 
            password='Qazssedc9', 
            host='localhost',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database.")
        print(e)
        exit()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def insert_json_data(cur, json_data, table, columns):
    for key, value in json_data.items():
        cur.execute(
            f"INSERT INTO public.{table} ({', '.join(columns)}) VALUES (%s, %s)", 
            (key, value)
        )
        print(f"Inserted {key} into the {table} table")

def main():
    conn = connect_db()
    cur = conn.cursor()
    
    domain_data = load_json('TaskManager_outputs/ClassDomains.json')
    insert_json_data(cur, domain_data, "class_domains", ["import", "type"])

    ast_data = load_json('TaskManager_outputs/AST.json')
    cur.execute("INSERT INTO public.ast (ast_data) VALUES (%s)", [Json(ast_data)])
    print("Inserted into the AST table")

    summary_data = load_json('TaskManager_outputs/ClassSummary.json')
    insert_json_data(cur, summary_data, "class_summary", ["class_name", "description"])

    documentation_data = load_json('TaskManager_outputs/Documentation.json')
    insert_json_data(cur, documentation_data, "documentation", ["import", "documentation"])

    func_domain_data = load_json('TaskManager_outputs/FunctionDomains.json')
    insert_json_data(cur, func_domain_data, "function_domain", ["function_", "domain_"])

    function_data = load_json('TaskManager_outputs/Functions.json')
    for key, info in function_data.items():
        cur.execute(
            "INSERT INTO public.functions (key, class_name, function_name, description) VALUES (%s, %s, %s, %s)",
            (key, info['class'], info['function'], info['description'])
        )
        print(f"Inserted {key} into the functions table")

    similarity_data = load_json('TaskManager_outputs/Similarities.json')
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

if __name__ == "__main__":
    main()
