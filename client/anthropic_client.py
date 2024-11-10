from anthropic import Anthropic
from .gptclient import GptClient
import json
from typing import List, Dict, Any
import logging
import re
import json

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
    
    def chat_with_model(self, messages: List[Dict[str, Any]], max_turns: int = 5) -> str:
        if max_turns <= 0:
            return "Max turns reached. Ending conversation."

        message = self.chat(
            messages=messages
        )

        text_func = extract_function_call(message.content[0].text)

        if text_func:
            for text_func_i in text_func:
                function_name = text_func_i['function_name']
                function_args = text_func_i['args'] or {}
                func = {'function':{'name':function_name, 'arguments':function_args}};

                result = self.use_tools([func])
                messages.append({"role": "assistant", "content": 'Tool Use: '+ function_name + "(" + json.dumps(function_args) +")"})
                messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "type": "tool_result",
                        "tool_use_id": function_name,
                        "content":str(result)
                    }),
                })

                return self.chat_with_model(messages, max_turns - 1)

        elif message.stop_reason == 'tool_use':
            # Handle tool calls
            for i in range(1, len(message.content)):
                function_name = message.content[i].name
                function_args = message.content[i].input

                func = {'function':{'name':function_name, 'arguments':function_args}};

                result = self.use_tools([func])

                messages.append({"role": "assistant", "content": 'Tool Use: '+ function_name + "(" + json.dumps(function_args) +")"})
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

def extract_function_call(text):
    results = []
    # Split by "Tool Use:" to get all tool uses
    tool_uses = text.split("Tool Use:")
    
    for tool_use in tool_uses[1:]:  # Skip first empty part
        tool_use = tool_use.strip()
        if not tool_use:
            continue
            
        # Find function name (text before first parenthesis)
        open_paren = tool_use.find('(')
        if open_paren == -1:
            continue
            
        function_name = tool_use[:open_paren].strip()
        
        # Find matching closing parenthesis
        stack = []
        args_end = -1
        for i, char in enumerate(tool_use[open_paren:], start=open_paren):
            if char == '(':
                stack.append(char)
            elif char == ')':
                stack.pop()
                if not stack:  # Found matching closing parenthesis
                    args_end = i
                    break
                    
        if args_end == -1:  # No matching closing parenthesis found
            continue
            
        # Extract arguments string
        args_str = tool_use[open_paren + 1:args_end]
        
        try:
            # Try to parse arguments as JSON
            args = json.loads(args_str)
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw string
            args = args_str
            
        results.append({
            'function_name': function_name,
            'args': args
        })
    
    if (results):
        return results
    else:
        return None
