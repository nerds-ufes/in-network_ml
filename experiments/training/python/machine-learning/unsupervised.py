import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster, datasets

path = '../results'
df1 = pd.read_csv('{}/dataset.csv'.format(path), delimiter=',')

k_means = cluster.KMeans(n_clusters=3)
k_means.fit(df1) 
df1['label'] =  k_means.labels_
X = df1.drop(columns=['TCPFlags'])

X.to_csv("{}/dataset_labeled.csv".format(path),sep=',', encoding='utf-8', index=False)
