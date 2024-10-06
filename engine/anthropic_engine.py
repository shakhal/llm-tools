import json
from typing import List, Dict, Any
import logging
from .gpt_engine import GptEngine

class AnthropicEngine(GptEngine):
    def __init__(self, client, prompt):
        super().__init__(client, prompt)
        self.client = client

    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        message = self.client.chat(
            messages=messages
        )

        if message.stop_reason == 'tool_use':
            # Handle tool calls
            for i in range(1, len(message.content)):
                function_name = message.content[i].name
                function_args = message.content[i].input

                func = {'function':{'name':function_name, 'arguments':function_args}};

                result = self.client.use_tools([func])

                messages.append({"role": "assistant", "content": 'Tool Use: '+message.content[i].name + "(" + json.dumps(message.content[i].input) +")"})
                messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "type": "tool_result",
                        "tool_use_id": message.content[i].id,
                        "content":str(result)
                    }),
                })

            # Recursive call to handle the tool response
            return self.chat_with_model(messages, max_turns - 1)
        else:
            # Regular text response
            return message.content[0].text

