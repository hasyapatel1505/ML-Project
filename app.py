
import pandas as pd
import streamlit as st
import pickle

import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"  # replace with your real API key

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path and poster_path.strip():
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            # fallback image when poster not available
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/500x750?text=Timeout"
    except requests.exceptions.RequestException as e:
        print(f"Request failed for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), key=lambda x: float(x[1]), reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommend System')
selected_movie_name = st.selectbox(
    'Which movie do you want to recommend?',
    movies['title'].values
)
if st.button('Recommend Movie'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3 ,col4,col5 = st.columns(5)

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