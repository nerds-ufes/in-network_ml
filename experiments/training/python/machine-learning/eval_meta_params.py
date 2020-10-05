import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import argparse


def get_full_rbf_dt_clf(train_x, train_y, param):
    clf = DecisionTreeClassifier() 
    grid = GridSearchCV(clf, param, n_jobs=-1)
    grid.fit(train_x, train_y)
    print(grid.best_estimator_)
    print("The best parameters are %s with a score of %0.2f" % (grid.best_params_, grid.best_score_))
    
    return clf, grid

def evaluate(f_in):
    print ('reading datasets')


    df = f_in
    X = None
    X = df.drop(columns=['label'])
    y = df['label'].values

    parameters = {'min_samples_leaf': [2,3,4,5,6]
        , 'min_samples_split': [2, 3]
        , 'max_leaf_nodes': [25]
        , 'min_impurity_decrease': [0.0003, 0.0004, 0.0005]
        }

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

    clf, grid = get_full_rbf_dt_clf(X_train, y_train, parameters)


    clf = grid.best_estimator_

    clf.fit(X_train, y_train)

    predicted = clf.predict(X_test)
    print ('RF: %f' % clf.score(X_test, y_test))
    print(classification_report(y_test, predicted))
    print(clf.get_params())

if __name__ == "__main__":

    pd.set_option('precision', 4)
    parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
    parser.add_argument('-pkt', help='Evaluate packet dataset', action='store_true', default=False, dest='pkt')
    parser.add_argument('-flow', help='Evaluate flow dataset', action='store_true', default=False, dest='flow')
    parser.add_argument('-sec', help='Evaluate flow dataset', action='store_true', default=False, dest='sec')
    args = parser.parse_args()

    if args.pkt:
        print ('Evaluate packet dataset')
        print ('reading datasets')
        df = pd.read_csv('../results/dataset_pkt_amostra.csv')
        X = df.drop(columns=['Unnamed: 0', 'idx_fw', 'idx_bw', 'src', 'dst', 'UDPSrcPort', 'ipS','ipD'])
        evaluate(X)
    if args.flow:
        print ('Evaluate flow dataset')
        print ('reading datasets')
        df = pd.read_csv('../results/dataset_flow1.csv')
        evaluate(df)
    if args.sec:
        print ('Evaluate flow dataset')
        print ('reading datasets')
        df = pd.read_csv('../results/dataset_session2.csv')
        X = df.drop(columns=['idx_fw', 'idx_bw', 'src', 'UDPSrcPort', 'ipS','ipD'])
        evaluate(X)