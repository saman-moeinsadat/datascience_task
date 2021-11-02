#!/bin/sh

if [ ! -f glove.6B/glove.6B.300d.txt ]; then
    echo "Make glove, not tar!"
    wget http://nlp.stanford.edu/data/glove.6B.zip
    unzip glove.6B.zip
fi
