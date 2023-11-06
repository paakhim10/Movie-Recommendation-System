
import streamlit as st

import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('/Users/paakhim10/Desktop/movie_recommender/movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)#dataframe with id,title,tags

similarity=pickle.load(open('/Users/paakhim10/Desktop/movie_recommender/similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'Select Movie',movies['title'].values
)

def fetch_poster(movie_id):
    data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f0ac80516edd242622d9ea2223bb9a27&language=en-US'.format(movie_id))
    data=data.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
def recommend(movie):
  movie_index=movies[movies['title'] ==movie].index[0]
  distances=similarity[movie_index] #gives a list of all distances for a movie
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6] #since we want top 5 recommendations

  m=[]
  p=[]
  #movies_list will return tuple with index of movie and dist corres
  for i in movies_list:
    m_id=movies.iloc[i[0]].movie_id
    #fetch poster from api
    p.append(fetch_poster(m_id))
    m.append((movies.iloc[i[0]].title))
    #print(i[0])
  return m,p

if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])

