from openai import OpenAI

class RequestAI:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def getRequest(self, text):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        result = response.choices[0].message.content.strip()
        return result