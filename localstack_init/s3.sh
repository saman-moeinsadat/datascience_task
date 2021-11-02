#!/bin/sh
echo "Init localstack s3"
awslocal s3 mb s3://s3-bucket
awslocal s3 cp /tmp/localstack/blocked.json s3://s3-bucket/blocked.json
awslocal s3 cp /tmp/localstack/currated.json s3://s3-bucket/currated.json
# awslocal s3 cp /tmp/localstack/word2vec.model.vectors.npy s3://s3-bucket/word2vec.model.vectors.npy
# awslocal s3 cp /tmp/localstack/word2vec.model s3://s3-bucket/word2vec.model

