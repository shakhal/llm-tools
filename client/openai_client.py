import openai
from .gptclient import GptClient

class OpenAiClient(GptClient):
    def __init__(self, model, tools_schema, apikey, base_url):
        super().__init__(tools_schema)
        self.model = model
        self.apikey = apikey
        self.tools_schema = tools_schema
        self.client = openai.OpenAI(
            base_url = base_url,
            api_key=apikey, 
        )


    def chat(self, messages):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools_schema,
        )
        