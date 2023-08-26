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

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaperaccess.com/full/2890760.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


st.title('One Stop Book Shop')
st.markdown("Search for your favourite books")

# Selectbox for choosing genre
genre_options = ["All Genres", "Fiction", "Non-fiction", "Science Fiction", "Mystery", "Fantasy",
                 "Autobiography", "Biography", "Romance", "Thriller", "Horror"]
selected_genre = st.selectbox("Select Genre:", genre_options)

# Handle genre selection
if selected_genre == "All Genres":
    genre_query = None
else:
    genre_query = selected_genre

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
    title = f'<a href="https://openlibrary.org/{book["key"]}">{book["title_suggest"]}</a>'
    year_of_publication = book.get('first_publish_year', 'N/A')
    book_data.append({
        'Cover': f'<img src="{cover_url}" width="100">',
        'Title': title,
        'Author': author_names,
        'Year of Publication': year_of_publication,
    })

# Create a DataFrame from the book_data list of dictionaries
#df = pd.DataFrame(book_data)
df = pd.DataFrame(book_data, index=range(1, len(book_data)+1), columns=['Cover', 'Title', 'Author', 'Year of Publication'])
st.markdown("""
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
    }
    .dataframe {
        border: 1px solid #d3d3d3;
        border-radius: 5px;
        background-color: #fff;
    }
    .dataframe a {
        text-decoration: none;
    }
    .dataframe a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)





html_table = df.to_html(escape=False)


# Display the HTML table using the st.markdown function
st.markdown(html_table, unsafe_allow_html=True)
