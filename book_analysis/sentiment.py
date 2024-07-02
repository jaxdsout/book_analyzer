import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit as st
from io import StringIO
analyzer = SentimentIntensityAnalyzer()


def sentimenter(file):
    stringio = StringIO(file.getvalue().decode("utf-8"))
    if stringio:
        text = stringio.read()
        breakdown = analyzer.polarity_scores(text)
        if breakdown["pos"] > breakdown["neg"]:
            return "It is a positive text"
        else:
            return "It is a negative text"


# CHAPTER SENTIMENT
def chap_sentimenter(file):
    stringio = StringIO(file.getvalue().decode("utf-8"))
    if stringio:
        text = stringio.read()
        pattern = re.compile("Chapter [0-9]+")
        chapters = re.split(pattern, text)
        chapters = chapters[1:]
        for nr, chapter in enumerate(chapters):
            breakdown = analyzer.polarity_scores(chapter)
            print(nr + 1, breakdown)





