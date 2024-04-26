import json

class StringToJson:
    def convert_to_json(string, outputPath):
        try:
            json_data = json.loads(string)
            # save to json file
            with open(outputPath, 'w') as f:
                json.dump(json_data, f)
            return json_data
        except json.JSONDecodeError:
            return None