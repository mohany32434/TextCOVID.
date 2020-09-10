import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text

module = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3") # Our model

# Takes in a list of questions and returns numpy arrays of their embeddings
def get_question_embeddings(questions):
    global module
    question_embeddings = module.signatures["question_encoder"](
        tf.constant(questions)
    )
    return question_embeddings["outputs"].numpy().astype(np.float32)

# Takes in a list of responses and returns numpy arrays of their embeddings
def get_response_embeddings(responses):
    global module
    response_embeddings = module.signatures["response_encoder"](
        input = tf.constant(responses),
        context = tf.constant(responses)
    )
    return response_embeddings["outputs"].numpy().astype(np.float32)
