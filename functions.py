import time
import platform
from duckduckgo_search import DDGS

def get_current_time() -> str:
    """Get the current time"""
    current_time = time.strftime("%A, %m/%d/%Y, %H:%M:%S")
    return f"The current time is {current_time}"

def get_system_info() -> str:
    """Get System Information"""
    return f"The system is {platform.system()} running on {platform.processor()}"

def query_duckduckgo(query: str) -> str:
    """
    Query the DuckDuckGo Instant Answer API and return the results.
    query: The search query to send to DuckDuckGo.
    Returns:
        A summary of the top result from DuckDuckGo.
    """
    results = DDGS().text(query, max_results=5)
    return results[0]

tools = [
  {
    'type': 'function',
    'function': {
      'name': 'get_current_time',
      'description': 'Get the current time',
      'parameters': {
        'type': 'object',
        'properties': {
        },
        'required': [],
      },
    },
  },
  {
    'type': 'function',
    'function': {
      'name': 'get_system_info',
      'description': 'Get System Information',
      'parameters': {
        'type': 'object',
        'properties': {
        },
        'required': [],
      },
    },
  },
  {
    'type': 'function',
    'function': {
      'name': 'query_duckduckgo',
      'description': 'Search the web using DuckDuckGo',
      'parameters': {
        'type': 'object',
        'properties': {
            "query": {
                "type": "string",
                "description": "the search query",
            },
        },
        'required': ['query'],
      },
    },
  },
]
