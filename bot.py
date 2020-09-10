import requests
import util
from config import *


class TelegramBot:
    """
    Utility class for managing the Telegram Bot
    """

    def __init__(self, webhook_url):
        """
        Initalizes both the class and the webhook
        """
        requests.get(webhook_url)

    def parse_webhook_data(self, webhook_data):
        """
        Parses the data coming in from telegram, and returns an appropriate response
        """
        message = webhook_data["message"]
        # Parse the data from message
        chat_id = message["chat"]["id"]
        incoming_message = message["text"].lower()
        # return the message
        return self.send_message(chat_id, util.get_answer_to_question(incoming_message))

    def send_message(self, chat_id, message):
        """
        Sends message to Telegram servers
        """
        res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(chat_id, message))
        if res.status_code == 200:
            return True
        return False
