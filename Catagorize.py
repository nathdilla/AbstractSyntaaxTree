import json
from RequestAI import RequestAI
from StringToJson import StringToJson

# Load the prompt from a file
with open('prompt.txt', 'r') as f:
    prompt = f.read()

function_command = "There are descriptions for each function in the json. Return a new json that has the function name as the key. For each value, get the corresponding label based on the function description. Just give me the json. nothing else."
class_command = "Given the description of each class, return a new json with the class name as the key. For each value, get the corresponding label based on the class description. Just give me the json. nothing else."

class Labeler:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def getFunctionDomain(self, functionJson, outputPath):
        # Load the documentation strings from a JSON file
        with open(functionJson, 'r') as f:
            data = json.load(f)
        request = RequestAI(self.api_key)
        result = request.getRequest(prompt + json.dumps(data) + function_command)
        StringToJson.convert_to_json(result, outputPath)
        return result
    
    def getClassDomain(self, classJson, outputPath):
        # Load the documentation strings from a JSON file
        with open(classJson, 'r') as f:
            data = json.load(f)
        request = RequestAI(self.api_key)
        result = request.getRequest(prompt + json.dumps(data) + class_command)
        StringToJson.convert_to_json(result, outputPath)
        return result
