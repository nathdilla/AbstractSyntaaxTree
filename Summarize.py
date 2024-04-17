from RequestAI import RequestAI
from StringToJson import StringToJson
import json

class Summarizer:
    def __init__(self, api_key):
        self.key = api_key
        self.requestAi = RequestAI(api_key)

    def summarizeClass(self, classJson, outputPath):
        with open(classJson, 'r') as file:
            data = json.load(file)
        class_str = json.dumps(data)
        request = self.requestAi.getRequest("Return a json with the class names and summarized class descriptions: " + class_str)
        StringToJson.convert_to_json(request, outputPath)
        return request
    
    def summarizeFunctions(self, functionJson, outputPath):
        with open(functionJson, 'r') as file:
            data = json.load(file)
        functions_str = json.dumps(data)
        request = self.requestAi.getRequest("Return a new json with just the function key and functions descriptions as the values. Summarize/simplify the descriptions: " + functions_str)
        StringToJson.convert_to_json(request, outputPath)
        return request

# Example usage
# api_key = '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'
# summarizer = Summarizer(api_key)
# results = summarizer.process_documentation()

# for result in results:
#     print(result)
