import numpy as np
import pandas as pd

from dataframes import MOVIES, RATINGS
from sklearn.neighbors import NearestNeighbors

def movie_neighbors_rec(id):
    row = MOVIES.index.get_loc(id)
    return pd.read_csv("data/tags_neighbors.csv", skiprows=[i for i in range(1, row+1)], nrows=1).iloc[0, 1:11]

def movie_similarity_rec(id):
    row = MOVIES.index.get_loc(id)
    result = pd.read_csv("data/tags_cosine_sim.csv", skiprows=[i for i in range(1, row+1)], nrows=1)
    return MOVIES.index[np.flipud(np.argsort(result.iloc[0,1:])[-10:])]

def actors_neighbors_rec(id):
    actors_neighbors = pd.read_csv("data/actors_neighbors.csv")
    return actors_neighbors[actors_neighbors['movieId']==id].drop('movieId', axis=1)

def overviews_similarity_rec(id):
    row = MOVIES.index.get_loc(id)
    result = pd.read_csv("data/overviews_cosine_sim.csv", skiprows=[i for i in range(1, row+1)], nrows=1)
    return MOVIES.index[np.flipud(np.argsort(result.iloc[0,1:])[-10:])]


def collaborative_rec(user):
    user_mean = user.fillna(np.random.randint(0, 5))
    print("USER MEAN: ", user_mean)
    nearest_neighbors = NearestNeighbors(n_neighbors=10, metric='euclidean').fit(RATINGS.fillna(np.random.randint(0, 5)))
    nearest_neighbors = nearest_neighbors.kneighbors(user_mean, return_distance=False)
    best_movies = RATINGS.iloc[nearest_neighbors[0]]
    print("BEST MOVIES: ", best_movies)
    best_movies = best_movies[best_movies.columns[user.iloc[0].isna()]]
    best_movies = best_movies.dropna(axis=1, how='all')
    best_movies = best_movies.mean().sort_values(ascending=False)
    return best_movies[:10].index