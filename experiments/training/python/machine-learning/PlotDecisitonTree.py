from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from IPython.display import Image  
import pydotplus
import os
import argparse

path = '../results'
p_tmp = '{}/tmp'.format(path)

def execute(df_train, df_test):
    X_train = df_train.drop(columns=['label'])
    y_train = df_train['label'].values
 
    X_test = df_test.drop(columns=['label'])
    y_test = df_test['label'].values
 
    clf = DecisionTreeClassifier(criterion='gini',
                       min_impurity_decrease=0.00001,
                       #min_impurity_decrease=0.005,
                       min_samples_leaf=2, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, splitter='best')

    clf.fit(X_train, y_train)
    predicted = clf.predict(X_test)

    print ('SCORE: %f' % clf.score(X_test, y_test))
    print(classification_report(y_test, predicted))

    from sklearn.externals import joblib
    filename = '{}/finalized_model_DT.sav'.format(p_tmp)
    joblib.dump(clf, filename)

    from sklearn.tree import export_graphviz
    cla = df1['label'].unique()[::-1]
    classes = []
    for c in np.sort(cla):
        classes.append(str(c))


    print (classes)
    export_graphviz(clf, out_file="{}/tree.dot".format(p_tmp), 
                    feature_names = X_train.columns,
                    class_names = classes,
                    rounded = True, proportion = False, 
                    precision = 3, filled = True)
    dot_data = export_graphviz(clf, out_file=None, 
                    feature_names = X_train.columns,
                    class_names = classes, 
                    rounded = True, proportion = False, 
                    precision = 3, filled = True, impurity=True)
    graph = pydotplus.graph_from_dot_data(dot_data)  
    Image(graph.create_png())
    graph.write_pdf("{}/tree.pdf".format(p_tmp))
    graph.write_png("{}/tree.png".format(p_tmp))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process to evaluate datasets.')
    parser.add_argument('-o', help='values pkt, flow or sec', default='pkt')
    args = parser.parse_args()


    try:
        os.mkdir(p_tmp)
    except OSError:
        print ("Creation of the directory tmp failed ")
    else:
        print ("Successfully created the directory tmp ")


    X_train = None
    X_test = None
    if args.o == 'pkt':
        params = ['Unnamed: 0', 'idx_fw', 'idx_bw', 'ipS','ipD', 'src', 'UDPSrcPort', 'UdpDstPort']

        df1 = pd.read_csv("{}/dataset_pkt_treino.csv".format(path))
        X_train = df1.drop(columns=params)

        df1 = pd.read_csv("{}/dataset_pkt_teste.csv".format(path))
        X_test = df1.drop(columns=params)

    if args.o == 'flow':
        params = ['idx_bw', 'src', 'UDPSrcPort', 'avg_len', 'len_variance', 'idx_fw','ipS','ipD', 'CumPacketSize',
        'CumIPv4Flag_Df','CumIPv4Flag_Mf','CumTcpFlag_Fin','CumTcpFlag_Syn','CumTcpFlag_Rst','CumTcpFlag_Psh','CumTcpFlag_Ack','CumTcpFlag_Urg', 'FlowDuration']

        df1 = pd.read_csv("{}/dataset_flow_treino2.csv".format(path), index_col='Unnamed: 0')
        print(df1.columns)
        X_train = df1.drop(columns=params)
        X_train = X_train.drop(columns=['20%'])

        df1 = pd.read_csv("{}/dataset_flow_teste.csv".format(path))
        X_test = df1.drop(columns=params)

    if args.o == 'sec':
        params = ['UDPSrcPort', 'ipS','ipD','src','idx_fw','idx_bw']

        df1 = pd.read_csv("{}/dataset_sec_treino.csv".format(path))
        X_train = df1.drop(columns=params)

        df1 = pd.read_csv("{}/dataset_sec_teste.csv".format(path))
        X_test = df1.drop(columns=params)

    execute(X_train, X_test)


'''
model = RandomForestClassifier(n_estimators=estimator,max_leaf_nodes=4, min_impurity_decrease=0.15)
model.fit(X, y)

from sklearn.tree import export_graphviz
classes = df1['label'].unique()[::-1]
ind = 0
for c in  model.estimators_:
    estimator = c
    name = 'tmp/treeRF{}'.format(ind)
    export_graphviz(estimator, out_file=name+'.dot', 
                    feature_names=X.columns,  
                    class_names = classes)

'''