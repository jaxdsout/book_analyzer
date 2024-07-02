import streamlit as st
from sentiment import sentimenter, chap_sentimenter
from freq_word import word_frequency
import pandas as pd
import requests

st.title("Book Analysis Megachad")
st.text("Need help deciding the feel of a text? Maybe the mood? \nHow about some good old stats? \n"
        "Figure out and upload your stuff now")
source_text = st.text_input("Search for a title: ")

def find_book():
    url = f"https://gutendex.com/books/?search={source_text}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        books = data.get("results", [])
        if books:
            top_10 = [
                {
                    'title': book.get('title', 'N/A'),
                    'author': ', '.join(author['name'] for author in book.get('authors', [])) or 'Unknown',
                    'link': book.get('formats', {}).get('text/plain; charset=us-ascii', '#')
                }
                for book in books[:10]
            ]
            return top_10
        else:
            return "No results found"
    else:
        print(f"Error: {response.status_code}")


if source_text is not None:
    results = find_book()
    for book in results:
        list_items = "\n".join([f"{book['title']}{book['link']}" for book in results])


    st.text("RESULTS:")
    st.text(f"{list_items}")


