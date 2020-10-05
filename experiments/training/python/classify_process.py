import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

print ('init')
df1 = pd.read_csv('../results/dataset_benign.csv')
df1['label'] = 'BENIGN'
df2 = pd.read_csv('../results/dataset_attack.csv')
df2['label'] = 'ATTACK'

frames = [df1, df2]
df = pd.concat(frames)
print('save df')
df.to_csv("../results/dataset_labeled.csv",sep=',', encoding='utf-8', index=False)


print('######## CLASSIFIER ########')
print( subprocess.Popen("python3 DecisionTree.py ", shell=True, stdout=subprocess.PIPE).stdout.read())


print('######## PlotDecisitonTree ########')
print( subprocess.Popen("python3 PlotDecisitonTree.py ", shell=True, stdout=subprocess.PIPE).stdout.read())

print('######## ifGenerator ########')
print( subprocess.Popen("python3 ifGenerator.py ", shell=True, stdout=subprocess.PIPE).stdout.read())
