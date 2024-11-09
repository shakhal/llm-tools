from .openai_llama_client import OpenAiLlamaClient
from .ollama_client import OllamaClient
from .openai_client import OpenAiClient  
from .anthropic_client import AnthropicClient
import logging
import json

class ClientProvider:
    def provide(type: str, model:str, tools:list, apikey:str, base_url:str = None):
        logging.debug("Tools:")
        logging.debug(json.dumps(tools, indent=4))
        if (type == 'openai'):
            return OpenAiClient(model, tools, apikey, base_url)
        if (type == 'openai-llama'):
            return OpenAiLlamaClient(model, tools, apikey, base_url)
        elif(type == 'ollama'):
            return OllamaClient(model, tools, apikey, base_url)
        elif(type == 'anthropic'):
            return AnthropicClient(model, tools, apikey, base_url)
