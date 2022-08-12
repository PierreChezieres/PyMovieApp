import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity


p = Pipeline(steps=[('scaler', StandardScaler()),
                    ('pca', PCA(n_components=500))])

tags = pd.read_csv('tags.csv', header=0, index_col='movieId')
tags_reduced = p.fit_transform(tags)
tags_dist, tags_neighbors = NearestNeighbors(n_neighbors=50, metric='euclidean').fit(tags_reduced).kneighbors(tags_reduced, return_distance=True)

tags_dist = pd.DataFrame(data=tags_dist, index=tags.index)

tags_neighbors = pd.DataFrame(data=tags_neighbors, index=tags.index)
tags_neighbors = tags_neighbors.replace(to_replace=np.arange(tags.shape[0]), value=tags.index)

tags_cosine_sim = cosine_similarity(tags_reduced)
tags_cosine_sim = pd.DataFrame(data=tags_cosine_sim, index=tags.index, columns=tags.index)

actors = pd.read_csv('actors.csv', header=0, index_col='movieId')
actors_dist, actors_neighbors = NearestNeighbors(n_neighbors=15, metric='jaccard').fit(actors).kneighbors(actors, return_distance=True)

actors_dist= pd.DataFrame(data=actors_dist, index=actors.index)

actors_neighbors = pd.DataFrame(data=actors_neighbors, index=actors.index)
actors_neighbors = actors_neighbors.replace(to_replace=np.arange(actors.shape[0]), value=actors.index)

tags_dist.to_csv('tags_dist.csv')
tags_neighbors.to_csv('tags_neighbors.csv')
tags_cosine_sim.to_csv('tags_cosine_sim.csv')
actors_dist.to_csv('actors_dist.csv')
actors_neighbors.to_csv('actors_neighbors.csv')