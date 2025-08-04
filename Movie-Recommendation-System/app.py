import streamlit as st
import pickle
import pandas as pd
import requests

import gdown
import os

BOW_SIMILARITY_FILE_ID = "1bXidFfCGzqpUBXLUkQSWjCIMV_ieKWqR"
@st.cache_data
def download_bow_similarity():
    url = f'https://drive.google.com/uc?id={BOW_SIMILARITY_FILE_ID}'
    output = 'bow_similarity.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output

TFIDF_SIMILARITY_FILE_ID = "1CJz-HpvSsXr9cZfG0NLXvKHITocC_MsU"
@st.cache_data
def download_tfidf_similarity():
    url = f'https://drive.google.com/uc?id={TFIDF_SIMILARITY_FILE_ID}'
    output = 'tfidf_similarity.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output

MOVIES_FILE_ID = "1qxoqQ9efwEJVLjbR5hbQhAyGH4vOgU4z"
@st.cache_data
def download_movies():
    url = f'https://drive.google.com/uc?id={MOVIES_FILE_ID}'
    output = 'movies_dict.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0f59d440ea5b3219284db8bf97a3f623&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    r_movies = []
    r_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        r_posters.append(fetch_poster(movie_id))
        r_movies.append(movies.iloc[i[0]].title)
        
    return r_movies, r_posters

st.title('Movie Recommernder System')

movies_path = download_movies()
movies_dict = pickle.load(open(movies_path, 'rb'))
movies = pd.DataFrame(movies_dict)

option = st.selectbox('Select a movie', movies['title'].values)

vectorizer = st.selectbox('Select Vectorizer', ['Bag of Words', 'TF-IDF'])
if vectorizer == 'Bag of Words':
    similarity_path = download_bow_similarity()
    similarity = pickle.load(open(similarity_path, 'rb'))
else:
    similarity_path = download_tfidf_similarity()
    similarity = pickle.load(open(similarity_path, 'rb'))    


if st.button('Recommend'):
    names, posters = recommend(option)
    st.write("Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])