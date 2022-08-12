import numpy as np
import pandas as pd


from pymovierec import *
from dataframes import *
from errors import *

import streamlit as st
from PIL import Image, ImageOps
import requests


import re


def find_movies(title):
    """_summary_

    Args:
        title (_type_): _description_

    Returns:
        _type_: _description_
    """
    return MOVIES[MOVIES['title'].str.contains(" ".join(title.split()), case=False)].index
    

def find_movies_component():
    input = st.text_input(label='Title', value='')
    if input=='':
        raise EmptyInputError
    else:
        movies = find_movies(input)
        if movies.empty:
            raise TitleNotFoundError(input)
        else:
            return movies


POSTER_RE = '^(https://image.tmdb.org/t/p/w500//)[\w\d]*(.jpg)$'
NO_POSTER = Image.open("no_poster_img.jpg").resize(size=(240, 320))

            
def draw_poster(id, parent=st, width=240, use_column_width='auto'):
    poster = POSTERS.loc[id, 'poster']
    title = MOVIES.loc[id, 'title']
    if (type(poster) is str) and (re.match(POSTER_RE, poster)):
        im = Image.open(requests.get(poster, stream=True).raw)
        im = im.resize(size=(240, 320))
        im = ImageOps.expand(im, border=1, fill='#262630')
        parent.image(im, caption=title, width=width, use_column_width=use_column_width)
    else:
        parent.image(NO_POSTER, caption=title, width=width, use_column_width=use_column_width)
        raise PosterError(title)

PICTURE_RE = '^(https://www.themoviedb.org/t/p/w300_and_h450_bestv2/)[\w\d]*(.jpg)$'
PICTURE_WIDTH = 80
MASK = Image.open('mask.png').convert('L').resize(size=(PICTURE_WIDTH, int(PICTURE_WIDTH*1.4)))


def draw_actor_pictures(id, parent=st, caption=''):
    actor_names = ACTOR_LIST[ACTOR_LIST['movieId']==id]['name']
    actor_ids = NAMES[NAMES['name'].isin(actor_names)].sort_values(by='name').index
    urls = PICTURES.loc[actor_ids, 'picture']
    missing_pictures = list()
    img_list = list()
    for i, url in enumerate(urls):
        if type(url) is str and re.match(PICTURE_RE, url):
            image = Image.open(requests.get(url, stream=True).raw)
            image = image.resize(size=(PICTURE_WIDTH, int(PICTURE_WIDTH*1.4)))
            image.putalpha(MASK)
            image = image.crop((0, 0, PICTURE_WIDTH, PICTURE_WIDTH))
            img_list.append(image)
        else:
            img_list.append(MASK.crop((0, 0, PICTURE_WIDTH, PICTURE_WIDTH)))
            missing_pictures.append(actor_names[i])            
    parent.image(img_list, caption=list(actor_names), width=PICTURE_WIDTH, use_column_width=False) 
    if len(missing_pictures)>1:
        raise ActorPictureError(missing_pictures)
    

def draw_ratings():
    if len(st.session_state) > 0:
        for movie in st.session_state:
            st.sidebar.write(f"{MOVIES.loc[int(movie), 'title']}") 
            star = int(st.session_state[movie])
            half_star = (st.session_state[movie] / 0.5) % 2
            movie_rating_container = st.sidebar.container()
            with movie_rating_container:
                cols = st.columns(5)
                for i in range(star):
                    with cols[i]: 
                        st.image('star.jpg')
                if half_star:
                    with cols[-1]:
                        st.image('half_star.jpg')

def run():
    st.title("Pymovie")

    st.header("Movie finder")
    
    try:
        movies = find_movies_component()[:10]
        finder = st.container()
        with finder:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                choice = st.radio(label='', options=movies, format_func=lambda id: MOVIES.loc[id, 'title'])
            with col2:
                try:
                    draw_poster(choice)
                except PosterError as pe:
                    st.sidebar.error(pe)
            with col3:
                try:
                    draw_actor_pictures(choice)
                except ActorPictureError as ape:
                    st.sidebar.error(ape)
                
                rating = st.slider(label='rating', min_value=0., max_value=5., step=0.5)
                save_rating = st.button(label="Rate & Save")
                
                if save_rating:
                    st.success("Rate saved")                    
                    st.session_state[choice] = rating
            draw_ratings()
                    
                
        st.header('Overview')
        row_overview = MOVIES.index.get_loc(choice)
        overview = pd.read_csv("data/overviews_text.csv", skiprows=[i for i in range(1, row_overview+1)], nrows=1)
        st.info(overview['overview'][0])




        st.header("Based on content")
        content_based = st.container()
        content_based_rec = movie_neighbors_rec(choice)
        with content_based:
            content_based_gallery_line1 = st.columns(5)
            for i, col in enumerate(content_based_gallery_line1):
                with col:
                    try: 
                        draw_poster(content_based_rec[i], use_column_width=False)
                    except PosterError as pe:
                        st.sidebar.error(pe)
            st.empty()
            content_based_gallery_line2 = st.columns(5)
            for i, col in enumerate(content_based_gallery_line2):
                with col:
                    try: 
                        draw_poster(content_based_rec[i+5], use_column_width=False)
                    except PosterError as pe:
                        st.sidebar.error(pe)            
            

        actors_based_rec = actors_neighbors_rec(choice)
        if len(actors_based_rec>0):
            st.header("Based on casting")
            actors_based = st.container()
            actors_based_rec = actors_neighbors_rec(choice).iloc[0]
            with actors_based:
                actors_based_gallery_line1 = st.columns(5)
                for i, col in enumerate(actors_based_gallery_line1):
                    with col:
                        try:
                            draw_poster(actors_based_rec[i], use_column_width=False)
                        except PosterError as pe:
                            st.sidebar.error(pe)
                st.empty()
                actors_based_gallery_line2 = st.columns(5)
                for i, col in enumerate(actors_based_gallery_line2):
                    with col:
                        try:
                            draw_poster(actors_based_rec[i+5], use_column_width=False)
                        except PosterError as pe:
                            st.sidebar.error(pe)
        else:
            st.warning(f"Unable to recommend movie based on {MOVIES.loc[choice, 'title']}")      
        
        st.header("Recommended for you")
        user = pd.DataFrame(columns=RATINGS.columns)
        for movie in st.session_state:
            user.loc[0, movie] = st.session_state[movie]
        collaborative = st.container()
        #collab_rec = collaborative_rec(np.random.choice(RATINGS.index))
        collab_rec = collaborative_rec(user)
        with collaborative:
            collaborative_gallery_line1 = st.columns(5)
            for i, col in enumerate(collaborative_gallery_line1):
                with col:
                    try: 
                        draw_poster(int(collab_rec[i]), use_column_width=False)
                    except PosterError as pe:
                        st.sidebar.error(pe)
            st.empty()
            collaborative_gallery_line2 = st.columns(5)
            for i, col in enumerate(collaborative_gallery_line2):
                with col:
                    try: 
                        draw_poster(int(collab_rec[i+5]), use_column_width=False)
                    except PosterError as pe:
                        st.sidebar.error(pe)  
                        
                        
    except EmptyInputError as aie:
        st.sidebar.error(aie)
    except TitleNotFoundError as tnfe:
        st.sidebar.error(tnfe)
       
run()