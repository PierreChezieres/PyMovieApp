import pandas as pd


TAGS = pd.read_csv("./data/tags.csv", header=0, index_col='movieId')
TITLES = pd.read_csv("./data/titles.csv", header=0, index_col='movieId')
YEARS = pd.read_csv("./data/years.csv", header=0, index_col='movieId')
POSTERS = pd.read_csv("./data/posters.csv", header=0, index_col='movieId')
OVERVIEWS = pd.read_csv("./data/overviews.csv", header=0, index_col='movieId')
ACTORS = pd.read_csv("./data/actors.csv", header=0, index_col='movieId')
PICTURES = pd.read_csv("./data/pictures.csv", header=0, index_col='actorId')
NAMES = pd.read_csv("./data/names.csv", header=0, index_col='actorId')
ACTOR_LIST = pd.read_csv("./data/actor_list.csv", header=0)