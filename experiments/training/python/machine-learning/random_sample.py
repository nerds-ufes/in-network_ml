import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV

print ('reading datasets')


df1 = pd.read_csv('../results/dataset_benign.csv')
df1['label'] = 'BENIGN'
df2 = pd.read_csv('../results/dataset_dos.csv')
df2['label'] = 'dos'
df3 = pd.read_csv('../results/dataset_hb.csv')
df3['label'] = 'heartbleed'
frames = [df1, df2, df3]

print ('join datasets')
df = pd.concat(frames)

print ('separate y')
X = df.drop(columns=['label'])
y = df['label'].values

print ('StratifiedShuffleSplit')
sss = StratifiedShuffleSplit(n_splits=1, test_size=110000, random_state=1)
print ('split')
print(sss.get_n_splits(X, y))

list = []
for train_index, test_index in sss.split(X, y):
    for index in test_index:
        list.append(df.iloc[index].values)

dts = pd.DataFrame(list, columns=df.columns)
dts = df.drop(columns=['ipsrc', 'ipdst'])

print ('saving')
dts.to_csv("../results/dataset_110000.csv",sep=',', encoding='utf-8', index=False)

