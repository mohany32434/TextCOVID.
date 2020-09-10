import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import *

authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version=WATSON_VERSION,
    authenticator=authenticator
)

assistant.set_service_url(WATSON_URL)

class WatsonSession:
    """
    Class to manage the IBM Watson session.  A session stores the state of a conversation.
    """

    def __init__(self):
        self.ssid = assistant.create_session(
            assistant_id=WATSON_ASSISTANT_ID
            ).get_result()['session_id']
        

    def get_response(self, text):
        """
        Returns the message from Watson Assistant in the current session.
        """
        response = assistant.message(
            assistant_id=WATSON_ASSISTANT_ID,
            session_id=self.ssid,
            input={
                "message_type": "text",
                "text": text
            }
        ).get_result()
        # Returns the response.  Change if you want more of the data for other things.
        return response["output"]["generic"][0]["text"]

    def close(self):
        """
        Deletes the current session
        """
        assistant.delete_session(
            assistant_id=WATSON_ASSISTANT_ID,
            session_id=self.ssid
        )
