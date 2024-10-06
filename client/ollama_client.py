import ollama
from .gptclient import GptClient

class OllamaClient(GptClient):
    def __init__(self, model, tools_schema, apikey, base_url):
        super().__init__(tools_schema)
        self.model = model
        self.apikey = apikey
        self.tools_schema = tools_schema
        self.client = ollama


    def chat(self, messages):
        return self.client.chat(
            model=self.model,
            messages=messages,
            tools=self.tools_schema,
        )
        