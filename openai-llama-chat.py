import logging
import argparse
from client.client_provider import ClientProvider
from engine.cli_runner import CliRunner
from prompts import prompt
from functions import tools
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Chatbot example')
    parser.add_argument('--logging', type=str, default='INFO', help='Logging level')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.logging, format='%(asctime)s - %(levelname)s - %(message)s')

    client = ClientProvider.provide("openai-llama", 'meta-llama/Meta-Llama-3.1-405B-Instruct-FP8', tools, os.getenv('OLLAMA_API_KEY'), os.getenv('OLLAMA_HOST'))
    CliRunner(client, prompt).run()

if __name__ == "__main__":
    main()
