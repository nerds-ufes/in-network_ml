from scapy.all import *
import pandas as pd
import numpy as np
from decimal import Decimal
import hashlib
import time
import argparse

def hash_md5(ips, tsp, tdp, ipd, usp, udp):
    hf = '{}{}{}{}{}{}'.format(ips, tsp, tdp, ipd, usp, udp)
    return hashlib.md5(hf.encode("utf-8")).hexdigest()




df = pd.read_csv("../results/dataset_session2.csv")
labeled = df[df['label'] == 'benign']
print(labeled['hdr.ipv4.totalLen'].mean(axis=0))

print(type(labeled['hdr.ipv4.totalLen'].mean(axis=0)))


print(int(labeled['hdr.ipv4.totalLen'].mean(axis=0)))

qt = int(labeled['hdr.ipv4.totalLen'].mean(axis=0))
sec = labeled[labeled['hdr.ipv4.totalLen'] == qt]

print(sec.sample(n=1))   
