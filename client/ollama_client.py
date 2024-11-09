import ollama
from .gptclient import GptClient
from typing import List, Dict, Any
import logging

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

    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        response = self.chat(
            messages=messages
        )
        
        message = response['message']

        if message['content'] == "":
            tools_calls = message['tool_calls']
            logging.debug("tools_calls")
            for tool in tools_calls:
                result = self.use_tools([tool])
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool['function']['name'],
                    "name": tool['function']['name'],
                    "content": str(result),
                })

            # Recursive call to handle the tool response
            return self.chat_with_model(messages, max_turns - 1)
        else:
          # Regular text response
          return message['content']