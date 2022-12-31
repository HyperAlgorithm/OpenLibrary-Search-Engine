import streamlit as st
import pandas as pd
import requests
from IPython.display import HTML

def search_books(query):
    # Use the requests library to make a GET request to the Open Library API
    #api_key = 'YOUR_API_KEY_HERE'
    url = f'https://openlibrary.org/search.json?q={query}'
    response = requests.get(url)
    
    # Parse the JSON response and extract the list of books
    data = response.json()
    books = data['docs']
    
    # Check if the docs list is empty
    if len(books) == 0:
        # If the docs list is empty, display a "Result not found" message
        st.markdown("Result not found")
    
    return books

st.title('One Stop Book Shop')
st.markdown("Search for your favourite books")
query = st.text_input('Enter a search query:')
results = []
if st.button('Search'):
    # Call the search function and store the results in a variable
    results = search_books(query)

# Create a list of dictionaries containing the cover image URLs, book titles, and author names
book_data = []
for book in results[:10]:
    # Check if the cover_i key is present in the JSON data
    if 'cover_i' in book:
        # If the cover_i key is present, use the cover image URL from the JSON data
        cover_url = f'https://covers.openlibrary.org/b/id/{book["cover_i"]}-M.jpg'
    else:
        # If the cover_i key is not present, use a default cover image URL
        cover_url = 'https://via.placeholder.com/100x150'
    # Join the author names with a comma separator
    author_names = ', '.join(book['author_name'])
    book_data.append({'Cover': f'<img src="{cover_url}" width="100">', 'Title': f'<a href="https://openlibrary.org/{book["key"]}">{book["title_suggest"]}</a>', 'Author': author_names})

# Create a DataFrame from the book_data list of dictionaries
#df = pd.DataFrame(book_data)
df = pd.DataFrame(book_data, index=range(1, len(book_data)+1))




html_table = df.to_html(escape=False)


# Display the HTML table using the st.markdown function
st.markdown(html_table, unsafe_allow_html=True)

