from pyngrok import ngrok

# Service Information
PORT = 5000

# Watson
WATSON_API_KEY = "[REPLACE THIS WIITH YOUR WATSON API KEY]"
WATSON_URL = "https://api.us-south.assistant.watson.cloud.ibm.com/instances/126e455d-f147-4cbc-b3c1-f4cf75e0064e"
WATSON_VERSION = "2020-04-01"
WATSON_ASSISTANT_ID = "[REPLACE THIS WIITH YOUR WATSON ASSISTANT ID]"

# Telegram
TOKEN = "[REPLACE THIS WIITH YOUR TELEGRAM BOT API KEY]"
NGROK_URL = ngrok.connect(port=PORT).replace("http://", "")
BASE_TELEGRAM_URL = "https://api.telegram.org/bot{}".format(TOKEN)
LOCAL_WEBHOOK_ENDPOINT = "{}/webhook".format(NGROK_URL)
TELEGRAM_INIT_WEBHOOK_URL = "{}/setWebhook?url={}".format(BASE_TELEGRAM_URL, LOCAL_WEBHOOK_ENDPOINT)
TELEGRAM_SEND_MESSAGE_URL = BASE_TELEGRAM_URL + "/sendMessage?chat_id={}&text={}"

# Database
PATH_TO_DATABASE = "[REPLACE THIS WITH THE FILE PATH TO YOUR responses.db FILE]"
