#!/bin/bash

# Why not use a dockerfile for everything?
# Because I prefer to set up the container using fabgis. And we want to
# avoid 42 layer limit.


sudo docker build -t linfiniti/projecta .
sudo docker run -p 7222:22 -p 7280:80 -t -d linfiniti/projecta
