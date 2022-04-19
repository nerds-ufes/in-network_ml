
============================= 
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

.. raw:: html
    <p float="left">
        <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmlast.png" height="400px"> 
        <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmfirst.png" width="400px"/> 
        <img src="https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmpacket.png" width="400px"/> 
    </p>




.. image:: https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmflow.png


.. image:: https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmflow_first.png

.. image:: https://github.com/nerds-ufes/in-network_ml/blob/main/figures/cmpkt.png
