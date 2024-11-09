from typing import Any, Dict, List
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
global_client = None
conversations: Dict[str, list] = {}

class SlackRunner:
    def __init__(self, client, prompt):
        self.client = client
        self.prompt = prompt
        global global_client
        global_client = client
        functions_desc = [ f["function"]["description"] for f in self.client.tools_schema]
        print("I am a chatbot able to do run some functions.", "Functions:\n\t",  "\n\t".join(functions_desc))
        print()

    def run(self):
        try:
            logging.info("Starting Slack bot...")
            handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
            logging.info("⚡️ Bolt app is running!")
            handler.start()
        except Exception as e:
            logging.error(f"Failed to start bot: {str(e)}", exc_info=True)
            raise


def get_or_create_conversation(channel_id: str) -> list:
    """Get existing conversation or create new one"""
    if channel_id not in conversations:
        logging.debug(f"Creating new conversation for channel: {channel_id}")
        conversations[channel_id] = []
    return conversations[channel_id]

@app.message()
def handle_direct_messages(message: Dict[str, Any], say: Any) -> None:
        """Handle all messages including DMs"""
        try:
            # Log the incoming message
            logging.debug(f"Received message: {message}")
            
            # Ignore bot's own messages
            if message.get("bot_id"):
                logging.debug("Ignoring bot message")
                return

            # Get channel/DM ID and message text
            channel_id = message["channel"]
            user_message = message["text"]
            
            logging.info(f"Processing message: {user_message} in channel: {channel_id}")
            
            handle_message(channel_id, user_message, say)
            
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}", exc_info=True)
            say(f"Sorry, I encountered an error: {str(e)}")

@app.event("app_mention")
def handle_mention(event: Dict[str, Any], say: Any) -> None:
    """Handle when the bot is mentioned in channels"""
    try:
        logging.debug(f"Received mention event: {event}")
        
        channel_id = event["channel"]
        user_message = event["text"].split(">", 1)[1].strip()
        
        logging.info(f"Processing mention: {user_message} in channel: {channel_id}")

        handle_message(channel_id, user_message, say)        
    
    except Exception as e:
        logging.error(f"Error processing mention: {str(e)}", exc_info=True)
        say(f"Sorry, I encountered an error: {str(e)}")

def handle_message(channel_id: str, user_message: str, say: Any) -> None: 
    # Get conversation history
    conversation = get_or_create_conversation(channel_id)
    
    # Add user message to history
    conversation.append({
        'role': 'user',
        'content': user_message
    })
    
    response = global_client.chat_with_model(conversation)
    logging.debug(f"Assistant: {response}")
    conversation.append({"role": "assistant", "content": response})

    # Send response
    say(response)
    logging.info("Response sent successfully")
