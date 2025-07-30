import streamlit as st
import pickle
import pandas as pd
import requests

# Page configuration
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    .main {
        padding-top: 0px;
        margin-top: 0px;
    }

    .header-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: black;
        margin-top: -10px;
    }

    .sub-header {
        text-align: center;
        font-size: 20px;
        color: #444;
        margin-top: -15px;
        margin-bottom: 20px;
    }

    .movie-container {
        width: 154px; 
        margin: 0 auto;
        text-align: center;
    }

    .movie-title {
        font-size: 14px;
        font-weight: 600;
        color: black;
        margin-top: 8px;
        line-height: 1.2em;
        /* Prevent line breaks inside words */
        word-wrap: break-word;
        hyphens: auto;
        white-space: normal;
    }

    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
    }

    .stButton>button:hover {
        background-color: #e60000;
    }

    .stSelectbox>div>div>div {
        background-color: #ffffff15;
    }
    </style>
""", unsafe_allow_html=True)

# --- Function to fetch poster URL ---
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0b8a27233ceec2b9a3bff51e42a261c8&language=en-US'
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w154" + data['poster_path']
    else:
        return "https://via.placeholder.com/154x231?text=No+Poster"

# --- Recommendation function ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for ii in movie_list:
        movie_id = movies.iloc[ii[0]].movie_id
        recommended_movies.append(movies.iloc[ii[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# --- Load data ---
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Title & subtitle ---
st.markdown('<div class="header-title">🎥 Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Find movies similar to your favorite one!</div>', unsafe_allow_html=True)

# --- Movie selection ---
selected_movie = st.selectbox("Select a movie:", movies['title'].values)

# --- Recommend button & display ---
if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    st.markdown("### 🔎 Recommended Movies")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            # Wrap image and title in a div with fixed width and center alignment
            st.markdown(
                f"""
                <div class="movie-container">
                    <img src="{posters[i]}" width="154" alt="{names[i]} poster" />
                    <div class="movie-title">{names[i]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
