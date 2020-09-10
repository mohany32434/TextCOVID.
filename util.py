from watsonapi import WatsonSession
from oracle.factbase import FactBase

sess = WatsonSession()
facts = FactBase()

starting_message = "This is the start of your conversation with our coronavirus chatbot.  This chatbot was developed for the New York Academy of Sciences' COVID-19 Challenge.  Please feel free to ask it any question.  If you would like to help combat the pandemic, please contribute to the Missing Maps project.  Please go to https://www.missingmaps.org/learn/ to learn more."

def get_answer_to_question(question):
    # starting message (The start of the chat)
    if question == "/start":
        return starting_message
    # Any question
    answer = sess.get_response(question)
    if answer == "I don't know the answer to that yet. But I am learning new things all the time.":
        answer = facts.get_best_answer(question)
    return answer
