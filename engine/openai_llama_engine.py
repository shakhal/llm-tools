import json
from typing import List, Dict, Any
import logging

class OpenAiLlamaEngine():
    def __init__(self, client, prompt):
        self.client = client

    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        response = self.client.chat(
            messages=messages
        )

        message = response.choices[0].message

        if "<|python_tag|>" in message.content:
            # Split and clean up the content to extract the JSON function calls
            function_calls_str = message.content.split("<|python_tag|>")[1].strip()
            
            # Split multiple function calls separated by semicolons
            function_calls = [call.strip() for call in function_calls_str.split(";") if call.strip()]
            
            for function_call_str in function_calls:
                # Parse the JSON function call
                function_call = json.loads(function_call_str)
                
                # Get function name and parameters
                function_name = function_call.get("name")
                function_args = function_call.get("parameters", {})
        
                func = {'function':{'name':function_name, 'arguments':function_args}};        
                result = self.client.use_tools([func])

                messages.append(message.model_dump())
                messages.append({
                    "role": "tool",
                    "name": function_name,
                    "content": str(result),
                })

            # Recursive call to handle the tool response
            return self.chat_with_model(messages, max_turns - 1)
        else:
            # Regular text response
            return message.content