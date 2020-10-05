#! /bin/bash

echo " "
echo " ****** Starting Experiment  ******************************"
echo " "

echo " "
echo " ****** PolKA Fabric Experiment  **************************"
echo " "
sudo ./p4app run experiments/sfc.p4app polka 1 10

echo " "
echo " ****** Sourcey Fabric Experiment  ************************"
echo " "
sudo ./p4app run experiments/sfc.p4app sourcey 1 10

echo " "
echo " ****** Experiment  Done***********************************"
echo " "
