
In-Network Machine Learning
=============================
In-network machine learning experiment repository.

Description
===========
This repository contains examples of how to push Machine Learning classification models for P4 switches into the Smartnics (Netronome).


Training directory
-------------------
It contains python3 scripts responsible for transforming data from pcap files, in models suitable for deployment in the network layer.


Smartnic directory
-------------------
It contains the source codes to run the experiments into the Smartnic Netronome (https://www.netronome.com/products/agilio-cx/)


Confusion Matrixes
------------------
Next Confusion Matrix graphics are relative to classification results achieved by *MAP4* in two proposed use-cases scenarios: (a) Intrusion Detection System (IDS), and; (b) Internet of Things (IoT).  

<p align="center">
  <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmlast.png" width="250" />
  <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmfirst.png" width="250" />
  <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmpacket.png" width="250" />
</p>  
CICIDS2017 Confusion matrices for: per-flow classification after the last (left) and the first (middle) packets of each flow are observed; and per-packet classification (right). Values are normalized by the sum of each row. 
<br/>
<br/>
<br/>
<br/>

<p align="center">
<img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmflow.png" />
<p/>
UNSW-IoT Confusion matrix per-flow classification after the last packets of each flow are observed.
<br/>
<br/>
<br/>
<br/>

<p align="center">
<img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmflow_first.png" />
<p/>
UNSW-IoT Confusion matrix per-flow classification after the first packets of each flow are observed.
<br/>
<br/>
<br/>
<br/>
<p align="center">
<img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmpkt.png" />
<p/>
UNSW-IoT Confusion matrix per-packet classification.
