import os
import re
import time
import json

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, render_template
from flask.logging import create_logger
from gensim.models import KeyedVectors


APP = Flask(__name__)
LOG = create_logger(APP)


@APP.route('/')
def home():
    return render_template('index1.html')


@APP.route("/mostSimilar/", methods=['POST'])
def find_similar():

    # converts the query word to lower case
    # and omits white space, under line and line.
    word = request.form["word"].strip().lower()
    word = re.sub("[' ', _, -]", '', word)

    # checking the currated.json file. 
    if word in APP.currated.keys():
        out_str = ', '.join([word.capitalize() for\
            word in APP.currated[word]])
        return render_template('index2.html', word=out_str)

    # checking the blocked.json file.
    elif word in APP.blocked:
        return render_template('index3.html',\
            word=word.capitalize())

    # using model to find word similarites and
    # catching exception, thrown by query word
    # not existing in app's dictionary.
    else:
        try:
            similars = APP.model.most_similar(positive=word)
            similars = ", ".join([sim[0].capitalize()\
                for sim in similars])

            return render_template('index4.html', similars=similars)

        except KeyError:
            return render_template('index5.html', word=word.capitalize())


# function for making S3 sevice wait for the model
# trained, being uploaded to s3 bucket.
def wait_for_s3(endpoint_url, bucket, key,\
    timeout=900, period=0.25):
    mustend = time.time() + timeout
    while time.time() < mustend:
        try:
            s3 = boto3.client('s3', endpoint_url=endpoint_url)
            s3.get_object(Bucket=bucket, Key=key[0])
            s3.get_object(Bucket=bucket, Key=key[1])
            return s3
        except Exception:
            time.sleep(period)
            LOG.info("Waiting for S3.....")
    raise Exception('S3 not reachable')


if __name__ == "__main__":
    endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
    bucket = os.environ.get("AWS_BUCKET_NAME")
    s3 = wait_for_s3(endpoint_url, bucket,\
        ['word2vec.model', 'word2vec.model.vectors.npy'])
    
    # downloading the currated.json and blocked.json from
    # s3 bucket.
    s3.download_file(bucket, 'blocked.json', 'blocked.json')
    s3.download_file(bucket, 'currated.json', 'currated.json')
    with open('currated.json') as currated_file:
        APP.currated = json.load(currated_file)
    with open('blocked.json') as blocked_file:
        APP.blocked = json.load(blocked_file)
    
    # downloading trained model from s3 bucket.
    s3.download_file(bucket, 'word2vec.model', 'word2vec.model')
    s3.download_file(bucket, 'word2vec.model.vectors.npy',\
        'word2vec.model.vectors.npy')

    # loading the model.
    APP.model = KeyedVectors.load("word2vec.model", mmap='r')

    APP.run(host="0.0.0.0", debug=True)
