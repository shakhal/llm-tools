import openai
from .gptclient import GptClient
from typing import List, Dict, Any
import logging
import json

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
        
    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        try:

            if max_turns <= 0:
                return "Max turns reached. Ending conversation."

            response = self.chat(
                messages=messages
            )

            message = response.choices[0].message

            if message.tool_calls:
                # Handle tool calls
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    func = {'function':{'name':function_name, 'arguments':function_args}};

                    result = self.use_tools([func])

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
        except Exception as e:
            print("messages", messages)
            logging.error(f"Error: {e}")
            return "An error occurred. Please try again later."