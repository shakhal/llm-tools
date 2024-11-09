# llm-tools

## Overview

`llm-tools` demonstrates using external tools (functions) with large language models (LLMs) such as OpenAI, Anthropic, and Ollama. This project provides a unified interface to interact with different LLMs, making it easier to switch between them and utilize their unique capabilities.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/shakhal/llm-tools.git
    cd llm-tools
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the Chatbots

Each chatbot script can be run from the command line. Below are example setups, and how to run each one:

#### OpenAI Chatbot

```sh
python openai-chat.py 
```

#### Anthropic Chatbot
```sh
python anthropic-chat.py
```

#### Ollama Chatbot
```sh
python ollama-chat.py
```

#### Ollama (using OpenAI Client) Chatbot
```sh
python openai-ollama-chat.py
```

#### Customizing Prompts and Tools
You can customize the prompts and tools used by editing the respective files:

* Prompts: prompts.py
* Tools: functions.py



