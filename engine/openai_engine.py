import json
from typing import List, Dict, Any
import logging
from .gpt_engine import GptEngine

class OpenAiEngine(GptEngine):
    def __init__(self, client, prompt):
        super().__init__(client, prompt)
        self.client = client

    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        response = self.client.chat(
            messages=messages
        )

        message = response.choices[0].message

        if message.tool_calls:
            # Handle tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                func = {'function':{'name':function_name, 'arguments':function_args}};

                result = self.client.use_tools([func])

                messages.append(message.model_dump())
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result),
                })

            # Recursive call to handle the tool response
            return self.chat_with_model(messages, max_turns - 1)
        else:
            # Regular text response
            return message.content
