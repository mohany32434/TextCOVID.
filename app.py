from flask import Flask, request, jsonify
from telegrambot import TelegramBot
from config import *
from pyngrok import ngrok
from util import sess, facts

# Iniitialize essentials
app = Flask(__name__)
bot = TelegramBot(TELEGRAM_INIT_WEBHOOK_URL)

@app.route("/webhook", methods=['POST'])
def webhook():
    """
    runs whenever there is a new message on telegram
    """
    req = request.get_json()
    success = bot.parse_webhook_data(req)
    return jsonify(success=success)

@app.route("/close")
def close():
    """
    Shuts down the flask server
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is not None: func()


if __name__ == "__main__":
    app.run(port=PORT)
    # Cleanup
    ngrok.disconnect(NGROK_URL)
    sess.close()
    facts.close()
