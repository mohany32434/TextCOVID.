import sys
sys.path.append("..")

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words
from oracle.database import open_database, update_database_with_sentences

# Initializing the summarizer class
language = "english"
stemmer = Stemmer(language)
summarizer = LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(language)

def update(urls):
    """
    Updates the database with sentences from the latest articles.
    """
    conn, c = open_database() # open database
    for url in urls:
        sentences = get_sentences(url)
        sentences = [str(sent) for sent in sentences]
        for sentence in sentences:
            print("Sentence added to FactBase:", sentence)
        update_database_with_sentences(c, conn, sentences, url)


def get_sentences(url, sentences_count=10):
    """
    Returns the important sentences given a url
    """
    parser = HtmlParser.from_url(url, Tokenizer(language))
    sentences = summarizer(parser.document, sentences_count)
    return sentences

# Insertion loop.  Enter URLs to articles you want to be auto-summarized and added to the database.
if __name__ == "__main__":
    urls = []
    inp = input("Enter an url: ")
    while inp != "done":
        urls.append(inp)
        inp = input("Enter an url: ")
    update(urls)
