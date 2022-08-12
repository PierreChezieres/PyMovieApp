import streamlit as st
import pandas as pd 

import numpy as np

from dataframes import TAGS, TITLES, YEARS, POSTERS, OVERVIEWS, ACTOR_LIST, NAMES, PICTURES
import content_based as cb


from utils import movies_to_str, movie_tags_info

from PIL import Image
import requests

from annotated_text import annotated_text

import re

TAGS_COLORS = ('#edf2f4',
               '#edf2f4',
               '#edf2f4',
               '#edf2f4',
               '#edf2f4',
               '#edf2f4',
               '#eae2b7',
               '#fcbf49',
               '#f77f00',
               '#d62828')

def colors_tags(tags):
    colored_tags = list()
    for tag in tags:
        level = tag[1]
        colored_tags.append((tag[0], str(level), TAGS_COLORS[level]))
    return colored_tags

TITLE = "PyMovie - Content Based Test"

st.set_page_config(page_title=TITLE, layout='wide')


class TitleNotFoundError(Exception):
    def __init__(self, title, message="Title not found !"):
        super().__init__(self)
        self.title = title
        self.message = message
        

    def __str__(self):
        return f"{self.title} : {self.message}"


class EmptyInputError(Exception):
    def __init__(self):
        super().__init__(self)
        self.message = "Remember...All I'm Offering Is The Truth. Nothing More."
    
    
    def __str__(self):
        return self.message


class PosterError(Exception):
    def __init__(self, title):
        super().__init__(self)
        self.message = f"Poster not available for {title}"
    
    
    def __str__(self):
        return self.message


def find_movies(title):
    return TITLES[TITLES['title'].str.contains(" ".join(title.split()), case=False)].index
    


def find_movies_component():
    title = st.sidebar.text_input(label='Movie title', value='',  key='movie_search')
    if title=='':
        raise EmptyInputError()
    else:   
        movies = find_movies(title)
        if movies.empty:   
            raise TitleNotFoundError(title)        
        else:
            options = movies_to_str(movies)
            with st.sidebar.expander('Select a movie...', expanded=True):
                choice = st.radio(label='', options=options, format_func=lambda x: x.split(']')[1])[:-7]
    return int(choice.split(']')[0][1:])


POSTER_RE = '^(https://image.tmdb.org/t/p/w500//)[\w\d]*(.jpg)$'
NO_POSTER = Image.open("no_poster_img.jpg").resize(size=(240, 320))

            
def draw_poster(id, parent=st, caption='', width=200, use_column_width='auto'):
    poster = POSTERS.loc[id, 'poster']
    title = TITLES.loc[id, 'title']
    if (type(poster) is str) and (re.match(POSTER_RE, poster)):
        im = Image.open(requests.get(poster, stream=True).raw)
        im = im.resize(size=(240, 320))
        parent.image(im, caption=caption, width=width, use_column_width=use_column_width)
    else:
        raise PosterError(title)
    

def draw_actor_pictures(id, parent=st, caption='', width=80):
    actor_names = ACTOR_LIST[ACTOR_LIST['movieId']==id]['name'].sort_values()
    actor_ids = NAMES[NAMES['name'].isin(actor_names)].sort_values(by='name').index
    urls = PICTURES.loc[actor_ids, 'picture']
    img_list = list()
    mask = Image.open('mask.png').convert('L')
    mask = mask.resize(size=(width, int(width*1.4)))
    for i, url in enumerate(urls):
        if type(url) is str:
            im = Image.open(requests.get(url, stream=True).raw)
            im = im.resize(size=(width, int(width*1.4)))
            im.putalpha(mask)
            img_list.append(im)
        else:
            img_list.append(mask)
    parent.image(img_list, caption=actor_names.tolist(), width=width, use_column_width=False)    

            
def run():
    st.title(TITLE)
    st.sidebar.header('Content Based Recommendation')
    
    try:      
        choice = find_movies_component()
        n_rec = st.sidebar.slider("Nb rec", min_value=1, max_value=20, value=10)
        data = st.sidebar.selectbox(label="Data", options=['tags', 'actors'])
        
        try:
            draw_poster(choice, parent=st.sidebar)
            draw_actor_pictures(choice, parent=st.sidebar)
        except PosterError as pe:            
            st.sidebar.image(NO_POSTER, width=200)
            st.sidebar.error(pe)
            
        
        
        st.sidebar.info(OVERVIEWS.loc[choice, 'overview'])
        
        with st.sidebar.expander("Tags"):
            tag_level = st.slider("Tag Level", 0, 9, value=9,  step=1)
            movie_infos = movie_tags_info(choice, level=tag_level)
            for tag in colors_tags(movie_infos):
                annotated_text(tag)
    
        
        with st.sidebar.expander("Options"):
            scaler = st.selectbox('Scaler', cb.SCALERS.keys())
            metric = st.selectbox('Metric', cb.METRICS)
        
        recommender = cb.NearestNeighborsRecommender(scaler=scaler, metric=metric, data=data)
        my_rec = recommender.rec(choice, n_rec)
        
        cols = st.columns(5)
        for i, movie_id in enumerate(my_rec):
            title = TITLES.loc[movie_id, 'title']
            with cols[i%5]:
                try:
                    draw_poster(id=movie_id, parent=st)
                except PosterError as pe:
                    st.sidebar.error(pe)
                    st.image(NO_POSTER)
                draw_actor_pictures(id=movie_id)
                with st.expander(title):
                    movie_rec_infos = movie_tags_info(movie_id, level=tag_level)
                    st.empty()
                    for tag in colors_tags(movie_rec_infos):
                        annotated_text(tag)
            st.container()
                
                               
    except TitleNotFoundError as tnfe:
        st.sidebar.error(tnfe)  
    except EmptyInputError as eie:
        st.sidebar.info(eie)
    
   
run()
