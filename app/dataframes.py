import pandas as pd


#tags_dist = pd.read_csv('data/tags_dist.csv', index_col='movieId')
#tags_neighbors = pd.read_csv('data/tags_neighbors.csv', index_col='movieId')
#tags_cosine_sim = pd.read_csv('data/tags_cosine_sim.csv', index_col='movieId')
#actors_dist = pd.read_csv('data/actors_dist.csv', index_col='movieId')
#actors_neighbors = pd.read_csv('data/actors_neighbors.csv', index_col='movieId')
#overviews_cosine_sim = pd.read_csv('data/overviews_cosine_sim.csv', index_col='movieId')

#MOVIES = pd.read_csv('data/movies.csv', index_col='movieId')
#tags = movies.drop(['title', 'year', 'imdbId'], axis=1)
#overviews = pd.read_csv('data/overviews.csv', index_col='movieId')
#POSTERS = pd.read_csv('data/posters.csv', index_col='movieId')
#PICTURES = pd.read_csv('data/pictures.csv', index_col='actorId')
#actors = pd.read_csv('data/actors.csv', index_col='movieId')
#NAMES = pd.read_csv('data/names.csv', index_col='actorId')
#ACTOR_LIST = pd.read_csv('data/actor_list.csv')
#RATINGS = ratings = pd.read_csv('data/ratings.csv', index_col='userId')

def load_data():
    NAMES = pd.read_csv('data/names.csv', index_col='actorId')
    ACTOR_LIST = pd.read_csv('data/actor_list.csv')
    RATINGS = ratings = pd.read_csv('data/ratings.csv', index_col='userId')
    POSTERS = pd.read_csv('data/posters.csv', index_col='movieId')
    PICTURES = pd.read_csv('data/pictures.csv', index_col='actorId')
    MOVIES = pd.read_csv('data/movies.csv', index_col='movieId')
    return NAMES, ACTOR_LIST, RATINGS, POSTERS, PICTURES, MOVIES

NAMES, ACTOR_LIST, RATINGS, POSTERS, PICTURES, MOVIES = load_data()

print("Chargement des dataframes - Terminé")