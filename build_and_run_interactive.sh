#!/bin/sh
tag="goit-pyweb-hw-02"
docker build -t $tag .
docker run -it $tag