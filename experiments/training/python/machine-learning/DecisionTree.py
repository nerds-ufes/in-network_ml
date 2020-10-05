import pandas as pd
import numpy as np
import sys

path = '../results'
df1 = pd.read_csv("{}/dataset_flow_treino2.csv".format(path))
X = df1.drop(columns=['label'])
y = df1['label'].values


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.multiclass import unique_labels
from sklearn.externals import joblib


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

rfor = RandomForestClassifier(n_estimators=1000, n_jobs=-1, verbose=1)
rfor.fit(X_train, y_train)

filename = '{}/finalized_model_flow.sav'.format(path)
joblib.dump(rfor, filename)

predicted = rfor.predict(X_test)
print ('RF: %f' % rfor.score(X_test, y_test))
print(classification_report(y_test, predicted))

loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, y_test)
print(result)
