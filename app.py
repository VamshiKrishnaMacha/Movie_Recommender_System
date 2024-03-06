import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    # Corrected the string formatting for movie_id
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=223aca5e63d9b6f36d322449d368e2ef')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # Corrected column name from 'movie_id' to 'id'
        movie_id = movies.iloc[i[0]]['id']  # Assuming 'id' is the correct column name
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Which movie do you like?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if len(names) > 0:
        with col1:
            st.text(names[0])
            st.image(posters[0])

    if len(names) > 1:
        with col2:
            st.text(names[1])
            st.image(posters[1])

    if len(names) > 2:
        with col3:
            st.text(names[2])
            st.image(posters[2])

    if len(names) > 3:
        with col4:
            st.text(names[3])
            st.image(posters[3])

    if len(names) > 4:
        with col5:
            st.text(names[4])
            st.image(posters[4])
