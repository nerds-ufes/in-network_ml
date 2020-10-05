#! /bin/bash

echo " "
echo " ****** Starting Experiment  ******************************"
echo " "

echo " "
echo " ****** PolKA Experiment  *********************************"
echo " "
sudo ./p4app run experiments/linear.p4app polka 0 10
echo " "
echo " ****** PolKA Fabric Experiment  **************************"
echo " "
sudo ./p4app run experiments/linear.p4app polka 1 10

echo " "
echo " ****** Sourcey Experiment  *******************************"
echo " "
sudo ./p4app run experiments/linear.p4app sourcey 0 10
echo " "
echo " ****** Sourcey Fabric Experiment  ************************"
echo " "
sudo ./p4app run experiments/linear.p4app sourcey 1 10


echo " "
echo " ****** PolKA Experiment  *********************************"
echo " "
sudo ./p4app run experiments/linear.p4app polka-var 0 10

echo " "
echo " ****** Experiment  Done***********************************"
echo " "
