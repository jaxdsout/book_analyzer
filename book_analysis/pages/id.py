import streamlit as st
import requests
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from io import StringIO
from nltk.corpus import stopwords


english_stopwords = stopwords.words("english")
analyzer = SentimentIntensityAnalyzer()


def word_frequency(url):
    response = requests.get(url)
    if response.status_code == 200:
        stringio = StringIO(response.text)
        text = stringio.read()
        pattern = re.compile("[a-zA-Z]+")
        findings = re.findall(pattern, text.lower())
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


def clean_subjects(subjects):
    cleaned_subjects = [subject.split(' -- ')[0] for subject in subjects]
    return cleaned_subjects


def show_details():
    book_id = st.session_state['book_id']
    print(book_id)
    if book_id is None:
        st.error("No book ID selected")
    else:
        url = f"https://gutendex.com/books/?ids={book_id}"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            book = response.json()
            if book.get('results'):
                book_data = book['results'][0]
                st.subheader("Book Details:")
                st.title(f"{book_data['title']}")
                author = ', '.join(authors['name'] for authors in book_data.get('authors', [])) or 'Unknown'
                st.subheader(f"by {author}")
                st.subheader("Subjects:")
                subjects = ', '.join(clean_subjects(book_data.get('subjects', [])))
                st.write(f"{subjects}")

                formats = book_data.get('formats', {})
                link = formats.get('text/plain; charset=us-ascii') or formats.get(
                    'text/html; charset=iso-8859-1') or 'N/A'
                sentiment = sentimenter(link)
                st.write(sentiment)

                freq = word_frequency(link)
                st.write(freq)
            else:
                st.error(f"No book found with ID: {book_id}")
        else:
            st.error(f"Error fetching book details. Status code: {response.status_code}")


if __name__ == "__main__":
    show_details()
