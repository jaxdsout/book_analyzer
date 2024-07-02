import re
from nltk.corpus import stopwords
english_stopwords = stopwords.words("english")


def word_frequency(file):
    book = file.read()
    pattern = re.compile("[a-zA-Z]+")
    findings = re.findall(pattern, book.lower())
    findings[:5]

    d = {}
    for word in findings:
        if word in d.keys():
            d[word] += 1
        else:
            d[word] = 1

    d_list = [(value, key) for (key, value) in d.items()]
    d_list = sorted(d_list, reverse=True)

    filtered_words = []
    for count, word in d_list:
        if word not in english_stopwords:
            filtered_words.append((word, count))
