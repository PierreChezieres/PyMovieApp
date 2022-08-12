import pandas as pd
import numpy as np
import streamlit as st
from dataframes import ACTORS, TAGS, TITLES, NAMES


from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.neighbors import NearestNeighbors


SCALERS = {
    'standard':StandardScaler(),
    'minmax':MinMaxScaler(),
    'maxabs':MaxAbsScaler(),
}


METRICS = ('euclidean', 'manhattan', 'chebyshev', 'hamming', 'canberra')


DATA = {
    'tags':TAGS,
    'actors':ACTORS
}


class NearestNeighborsRecommender():
    def __init__(self,
                 scaler='standard',
                 metric='euclidean',
                 data='tags'):
        self.scaler = SCALERS[scaler]
        self.metric = metric
        self.data = DATA[data]
        self.data_scaled = self.scaler.fit_transform(self.data)
        self.nearest_neighbors = NearestNeighbors(n_neighbors=20,
                                                  algorithm='auto',
                                                  metric=self.metric)
        self.nearest_neighbors.fit(self.data_scaled)
        

    def rec(self, id, n_rec=10):
        if n_rec not in range(1, 20):
            raise ValueError
        choice = self.data[self.data.index==id]
        choice = self.scaler.transform(choice)
        neighbors = self.nearest_neighbors.kneighbors(choice,
                                                      n_rec+1,
                                                      return_distance=False)
        return self.data.iloc[neighbors[0][1:n_rec+1]].index
        

    def rec_from_list(self, list_id):
        pass
