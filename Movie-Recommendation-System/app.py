import streamlit as st
import pickle
import pandas as pd
import requests

import gdown
import os

SIMILARITY_FILE_ID = "1Z3i_wogtNwHJYBdgnOYkJGf35Fr1YKxL"
@st.cache_data
def download_similarity():
    url = 'https://drive.google.com/uc?id={FILE_ID}.format(SIMILARITY_FILE_ID)'
    output = 'similarity.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return output

MOVIES_FILE_ID = "1qxoqQ9efwEJVLjbR5hbQhAyGH4vOgU4z"
@st.cache_data
def download_movies():
    url = 'https://drive.google.com/uc?id={FILE_ID}.format(MOVIES_FILE_ID)'
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


movies_path = download_movies()
movies_dict = pickle.load(open(movies_path, 'rb'))
movies = pd.DataFrame(movies_dict)

similarity_path = download_similarity()
similarity = pickle.load(open(similarity_path, 'rb'))

st.title('Movie Recommernder System')

option = st.selectbox('Select a movie', movies['title'].values)

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