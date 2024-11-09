import logging
import argparse
from client.client_provider import ClientProvider
from slack_bolt.adapter.socket_mode import SocketModeHandler
from engine.engine_provider import EngineProvider
from engine.cli_runner import CliRunner
from engine.slack_runner import SlackRunner
from prompts import prompt
from functions import tools
import os

def main():
    parser = argparse.ArgumentParser(description='Chatbot example')
    parser.add_argument('--logging', type=str, default='INFO', help='Logging level')
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=args.logging, format='%(asctime)s - %(levelname)s - %(message)s')

    client = ClientProvider.provide("openai", 'gpt-4o', tools, os.getenv('OPENAI_API_KEY'))
    engine = EngineProvider.provide("openai", client, prompt)
    SlackRunner(client, engine, prompt).run()


if __name__ == "__main__":
    main()
