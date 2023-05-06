import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5eb8cd228ef30963ff252f15ce1a8348&language=en-US'.format(movie_id))
    data = r.json()
    # st.text(data)
    # st.text('https://api.themoviedb.org/3/movie/{}?api_key=5eb8cd228ef30963ff252f15ce1a8348&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for a in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[a[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[a[0]].title)

    return recommended_movies, recommended_movies_posters


st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('how would you like to be contacted', movies['title'].values)

if st.button('Show Recommendation'):
    names, poster = recommend(selected_movie_name)
    # for i in recommendations:
    #     st.write(i)
    # names = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

