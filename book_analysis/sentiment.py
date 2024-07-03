import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from io import StringIO
analyzer = SentimentIntensityAnalyzer()


def sentimenter(url):
    response = requests.get(url)
    if response.status_code == 200:
        stringio = StringIO(response.text)
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





