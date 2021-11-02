import os
import re, unicodedata


import pandas as pd
import boto3
import inflect
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors
from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

from app import wait_for_s3

current_path = os.getcwd()
nltk.download('stopwords')
nltk.download('wordnet')


# removes punctuations and ascii characters and convert
# the string to lower case.
def lower_ascii_punctuation_removed(tokens):
    new_tokens = []
    for token in tokens:
        ascii_removed = unicodedata.normalize('NFKD', token).\
            encode('ascii', 'ignore').decode('utf-8', 'ignore').lower()

        punct_removed = re.sub(r'[^\w\s]', '', ascii_removed)

        if punct_removed != '':
            new_tokens.append(punct_removed)
            
    return new_tokens


def replace_numbers(words):
    """
    Replace all interger occurrences in list of tokenized
    words with textual representation
    """
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


# preprocesses the dataset and makes it ready for trainning
# wrapper function around above functions.
def preprocess_tokenize_text(str_sentence):
    links_removed = re.sub(r"http\S+", "", str_sentence)
    at_removed = re.sub(r"@\S+", "", links_removed)
    hashtag_removed = re.sub(r"#\S+", "", at_removed)
    tokenized_str = simple_preprocess(hashtag_removed,\
        deacc=True, max_len=300)
    tokenized_str = lower_ascii_punctuation_removed(tokenized_str)
    numbers_replaced = replace_numbers(tokenized_str)
    stopwords_removed = remove_stopwords(numbers_replaced)
    lemmatized = lemmatize_verbs(stopwords_removed)

    return lemmatized


# load glove word to vector embedding model and vectors
# for transfer learning of or embedding model.
def make_glove():
    glove_file = datapath(current_path +\
        "/glove.6B/glove.6B.300d.txt")
    tmp_file = get_tmpfile("test_word2vec.txt")

    _ = glove2word2vec(glove_file, tmp_file)

    glove_vectors = KeyedVectors.load_word2vec_format(tmp_file)

    return glove_vectors


def test_w2v_pos_neg(model, pairs):
    for (pos, neg) in pairs:
        math_result = model.most_similar(positive=pos, negative=neg)
        print(f'Positive - {pos}\tNegative - {neg}')
        [print(f"- {result[0]} ({round(result[1],5)})") \
            for result in math_result[:5]]
        print()


# transfer learning of word to vector model with our
# dataset
def train_glove(glove_vectors, threshold=10, min_count=20):

    print("Bulding the Corpus...")
    data = pd.read_csv(current_path + "/data/sample_data.csv", \
        encoding='iso8859_15')
    data['Tokenized'] = data['OriginalTweet'].\
        map(lambda x: preprocess_tokenize_text(x))
    documents = data['Tokenized']
    sentences = [sentence for sentence in documents if len(sentence) != 0]

    # get bigrams
    bigram = Phrases(sentences, min_count=min_count, threshold=threshold)
    bigram_phraser = Phraser(bigram)

    bigramed_tokens = []
    for sent in sentences:
        tokens = bigram_phraser[sent]
        bigramed_tokens.append(tokens)

    # run again to get trigrams
    trigram = Phrases(bigramed_tokens, min_count=min_count, \
        threshold=threshold)
    trigram_phraser = Phraser(trigram)

    trigramed_tokens = []
    for sent in bigramed_tokens:
        tokens = trigram_phraser[sent]
        trigramed_tokens.append(tokens)
    

    model = Word2Vec(vector_size=300, min_count=1)
    model.build_vocab(trigramed_tokens)
    total_examples = model.corpus_count

    # loading GloVe vectors and weights.
    model.build_vocab([list(glove_vectors.index_to_key)], update=True)

    print("Training...")
    model.train(trigramed_tokens, total_examples=total_examples, \
        epochs=model.epochs)
    model_wv = model.wv
    del model
    return model_wv


def test_w2v(model, pairs):
    for (pos, neg) in pairs:
        math_result = model.most_similar(positive=pos, negative=neg)
        print(f'Positive - {pos}\tNegative - {neg}')
        [print(f"- {result[0]} ({round(result[1],5)})") for \
            result in math_result[: 5]]
        print()


if __name__ == "__main__":
    print("Loading GLoVe...")
    glove_vectors = make_glove()
    model = train_glove(glove_vectors)
    print("Saving the model...")
    model.save(current_path + "/word2vec.model")
    endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
    bucket = os.environ.get("AWS_BUCKET_NAME")
    # creating s3 client.
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    print("Uploading the model...")
    # upload the model to s3 bucket.
    s3.upload_file(current_path+'/word2vec.model', bucket, \
        'word2vec.model')
    s3.upload_file(current_path+'/word2vec.model.vectors.npy', \
        bucket, 'word2vec.model.vectors.npy')

