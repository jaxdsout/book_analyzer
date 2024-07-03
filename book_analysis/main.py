import streamlit as st
import requests
st.set_page_config(initial_sidebar_state="collapsed")
st.title("Book Analysis Megachad")
st.text("Need help deciding the feel of a text? Maybe the mood? \nHow about some good old stats? \n"
        "Figure out and upload your stuff now")
st.subheader("SEARCH FOR TITLES:")
source_text = st.text_input("", label_visibility="collapsed")

if 'book_id' not in st.session_state:
    st.session_state['book_id'] = None


def find_books():
    if source_text:
        url = f"https://gutendex.com/books/?search={source_text}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            books = data.get("results", [])
            if books:
                search_results = [{
                    'id': book.get('id', 'No entry'),
                    'title': book.get('title', 'N/A'),
                    'author': ', '.join(author['name'] for author in book.get('authors', [])) or 'Unknown',
                    } for book in books]
                return search_results
            else:
                return []
        else:
            st.error(f"Error: {response.status_code}")
            return "No results found."
    return []


if __name__ == "__main__":
    results = find_books()
    if source_text and results:
        st.subheader("RESULTS:")
        for book in results[:10]:
            if st.page_link("pages/id.py", label=f"{book['title']} // {book['author']}"):
                st.session_state.book_id = book['id']
        if len(results) > 10:
            if st.button("NEED MORE RESULTS?"):
                for book in results[10:20]:
                    if st.page_link(f"pages/id.py", label=f" **{book['title']} // {book['author']}"):
                        st.session_state.book_id = book['id']

    else:
        st.text("Loading current top titles...")
