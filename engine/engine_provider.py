from .anthropic_engine import AnthropicEngine
from .olllama_engine import OllamaEngine
from .openai_engine import OpenAiEngine
from .openai_llama_engine import OpenAiLlamaEngine

class EngineProvider:
    def provide(type: str, client, prompt: str):
        if (type == 'anthropic'):
            return AnthropicEngine(client, prompt)
        elif(type == 'ollama'):
            return OllamaEngine(client, prompt)
        elif(type == 'openai'):
            return OpenAiEngine(client, prompt)
        elif(type == 'openai-llama'):
            return OpenAiLlamaEngine(client, prompt)