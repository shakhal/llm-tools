import logging
import argparse
from client.client_provider import ClientProvider
from engine.engine_provider import EngineProvider
from prompts import prompt
from functions import tools


def main():
    parser = argparse.ArgumentParser(description='Chatbot example')
    parser.add_argument('--logging', type=str, default='INFO', help='Logging level')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.logging, format='%(asctime)s - %(levelname)s - %(message)s')

    client = ClientProvider.provide("anthropic", 'claude-3-opus-20240229', tools, ANTHROPIC_API_KEY, None)
    engine = EngineProvider.provide("anthropic", client, prompt)
    engine.run();

if __name__ == "__main__":
    main()
