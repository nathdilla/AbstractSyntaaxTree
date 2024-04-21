import psycopg2
from psycopg2.extras import Json
import json

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname='pgPrinciples', 
    user='postgres', 
    password='Qazssedc9', 
    host='localhost',
    port=5432
)

if conn is None:
    print("Error: Unable to connect to the database.")
    exit()
else:
    print("Connected to the database")

cur = conn.cursor()

#------------------------------------------------------------
# read the ClassDomains.json file
with open('TaskManager_outputs/ClassDomains.json', 'r') as file:
    domain_data = json.load(file)

# Insert the data into the table
for key, value in domain_data.items():
    cur.execute("""
                INSERT INTO public."ClassDomains" (import, type) VALUES (%s, %s)
                """
                , (key, value))
    print(f"Inserted {key} into the ClassDomains table")

#------------------------------------------------------------
# Read the AST.json file
with open('TaskManager_outputs/AST.json', 'r') as file:
    ast_data = json.load(file)

# Insert the data into the table
for i in range(1):
    cur.execute("""
                INSERT INTO public.ast (ast_data) VALUES (%s)
                """
                , [Json(ast_data)])
    print(f"Inserted into the AST table")
    

#------------------------------------------------------------
# read the ClassSummary.json file
with open('TaskManager_outputs/ClassSummary.json', 'r') as file:
    summary_data = json.load(file)

# Insert the data into the table
for key, value in summary_data.items():
    cur.execute("""
                INSERT INTO public.class_summary (class_name, description) VALUES (%s, %s)
                """
                , (key, value))
    print(f"Inserted {key} into the class summary table")

#------------------------------------------------------------
# read the Documentation.json file
with open('TaskManager_outputs/Documentation.json', 'r') as file:
    documentation_data = json.load(file)

# Insert the data into the table
for key, value in documentation_data.items():
    cur.execute("""
                INSERT INTO public.documentation (import, documentation) VALUES (%s, %s)
                """
                , (key, value))
    print(f"Inserted {key} into the class summary table")

#------------------------------------------------------------
# read the FunctionDomains.json file
with open('TaskManager_outputs/FunctionDomains.json', 'r') as file:
    funcDomain_data = json.load(file)

# Insert the data into the table
for key, value in funcDomain_data.items():
    cur.execute("""
                INSERT INTO public.function_domain (function_, domain_) VALUES (%s, %s)
                """
                , (key, value))
    print(f"Inserted {key} into the class summary table")

#------------------------------------------------------------
# read the Functions.json file
with open('TaskManager_outputs/Functions.json', 'r') as file:
    function_data = json.load(file)

# Insert the data into the table
for key, info in function_data.items():
    cur.execute("""
                INSERT INTO public.functions (key, class_name, function_name, description) VALUES (%s, %s, %s, %s)
                """
                , (key, info['class'], info['function'], info['description'])
                )
    print(f"Inserted {key} into the functions table")

#------------------------------------------------------------
with open('TaskManager_outputs/Similarities.json', 'r') as file:
    similarity_data = json.load(file)

# Insert the data into the table
for class_name, tests in similarity_data.items():
        for test_name, category in tests.items():
            cur.execute(
                "INSERT INTO similarities (class_name, test_name, category) VALUES (%s, %s, %s)",
                (class_name, test_name, category)
            )    
            print(f"Inserted {test_name} into the similarities table")


# Commit the transaction
conn.commit()

# Close the connection
cur.close()
conn.close()
