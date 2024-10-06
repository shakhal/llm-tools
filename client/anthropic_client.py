from anthropic import Anthropic
from .gptclient import GptClient

class AnthropicClient(GptClient):
    def __init__(self, model, tools_schema, apikey, base_url):
        super().__init__(tools_schema)
        tools = [f['function'] for f in tools_schema]
        for f in tools:
            f['input_schema'] = f['parameters']
            del f['parameters']

        self.model = model
        self.apikey = apikey
        self.tools_schema = tools_schema;
        self.anthropic_tools = tools
        self.client = Anthropic(
            api_key=apikey,
        )
        

    def chat(self, messages):
        if messages and messages[0]["role"] == "system":
            system = messages.pop(0)["content"]
        else:
            system = ""

        return self.client.messages.create(
            max_tokens=1024,
            system=system,
            model=self.model,
            messages=messages,
            tools=self.anthropic_tools,
        )
        