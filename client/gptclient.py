from functions import *
import logging

class GptClient():
    def __init__(self, tools):
        self.tool_functions = {function["function"]["name"]: globals()[function["function"]["name"]]  for function in tools }

        
    def use_tools(self, tools_calls):
        tools_responses = []
        for tool_call in tools_calls:
            # Parse tool name and arguments
            tool_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            # Dynamically call the function
            if tool_name in self.tool_functions:
                try:
                    logging.info(f"Calling function: {tool_name}")
                    result = self.tool_functions[tool_name](**arguments)
                    tools_responses.append(str(result))
                except Exception as error:
                    tools_responses.append(str(error))
            else:
                raise KeyError(f"Function {tool_name} not found in the provided tool functions.")
        return "\n".join(tools_responses)

