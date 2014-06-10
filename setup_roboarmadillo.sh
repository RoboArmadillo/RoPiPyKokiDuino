#!/bin/bash

sudo apt-get install libopencv-dev libyaml-dev freeglut3-dev scons python-picamera python-rpi.gpio python-serial python-opencv
cd libkoki
sudo chmod 755 create-pkg-config
sudo scons
sudo mv lib/libkoki.so /usr/lib
cd ..
cd PiPyKoki
sudo python setup.py install
