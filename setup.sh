#!/bin/sh

if [ ! -f glove.6B/glove.6B.300d.txt ]; then
    echo "Make glove, not tar!"
    wget http://nlp.stanford.edu/data/glove.6B.zip
    unzip glove.6B.zip
    mkdir glove.6B
    rm glove.6B.50d.txt
    rm glove.6B.100d.txt
    rm glove.6B.200d.txt
    mv glove.6B.300d.txt ./glove.6B
    rm -r glove.6B.zip
fi
