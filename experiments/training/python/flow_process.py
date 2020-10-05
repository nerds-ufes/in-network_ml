import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import argparse
import shlex

print ('init')
parser = argparse.ArgumentParser(description='Flow process to join/extract features/train classifier.')
parser.add_argument('-j', help='Join pcap files', action='store_true', default=False, dest='join')
parser.add_argument('-ef', help='Extract Features', action='store_true', default=False, dest='extra')
parser.add_argument('-em', help='Evaluate meta params (cross-validation)', action='store_true', default=False, dest='eval')

args = parser.parse_args()

print (args)

def execute(command):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE,bufsize=1)
    lines_iterator = iter(popen.stdout.readline, b"")
    while popen.poll() is None:
        for line in lines_iterator:
            nline = line.rstrip()
            print(nline.decode("latin"), end = "\r\n",flush =True) # yield line


execute(['echo',  'Hello \nstdout'] )


if args.join:
    print('######## Join pcap files ########')
    execute(["python3",  "utils/join_pcap.py"])


if args.extra:
    print('######## Extract Features ########')
    execute(["python3",  "utils/show.py"])

if args.eval:
    print('######## Evaluate meta params (cross-validation) ########')
    execute(["python3", "eval_meta_params.py"])
