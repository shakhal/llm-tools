import json
from typing import List, Dict, Any
import logging
from .gpt_engine import GptEngine

class OllamaEngine(GptEngine):
    def __init__(self, client, prompt):
        super().__init__(client, prompt)
        self.client = client

    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        response = self.client.chat(
            messages=messages
        )
        
        message = response['message']

        if message['content'] == "":
            tools_calls = message['tool_calls']
            logging.debug("tools_calls")
            for tool in tools_calls:
                result = self.client.use_tools([tool])
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