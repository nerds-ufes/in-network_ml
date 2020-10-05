import numpy as np
import pandas as pd


path = 'results'
df1 = pd.read_csv("{}/iris.csv".format(path))

columns = {}
for c in df1.columns:
    columns[c] = c.replace(" ", "")

df1.rename(columns=columns, inplace=True)   
X = df1.drop(columns=['target'])
y = df1['target'].values

for index, row in df1.iterrows():
*if*