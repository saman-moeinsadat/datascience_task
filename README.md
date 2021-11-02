# Find Similar Words

## Setup

This application uses GloVe pre-trained vectors and weights for the purpose of training a word to vector model. For downloading GloVe vectors please run this command: 
```
./setup.sh
```
Please note that running this command is necessary, only the first time deploying the docker container, afterwards the bash file checks for existence of GloVe model and if it exists, does not download the model again. 

## Serve Application

For deploying the application locally please run this command: 
```
docker-compose up --build
```

Plaese note that this container includes three separate servies:
- train: Trains the model and passes the trained model to s3 bucket.
- s3: Simple storage unit for uploading and downloading files between containers.
- app: Finds similar words for a given query word and checks blocked and currated list for existence of the query word.

## Further Suggestions

The dataset used for training our model is quite small in comparison to real world data and taking additional actions is necessary for scaling this application. These actions include:
- The number of dimentions in our vector space must be chosen very carefully to prevent expensive and heavy calculations.
- Finding similar words for a given query word includes calculating similarity score(can be euclidean distance) between query word and all the words in our dictionary and is too expensive. Instead the vectors(words) can be clustered using K-mean Clustering technic or Hierarchical clustering to present us with insights for discovering and visualizing groups of words which all are closely related. In the case of K-mean Clustering, first we need to calculate the distance between query word and the mean of each cluster and after finding the cluster of words which are closely realated to query word, we need to calculate the similarity score only between query word and words contain in that cluster. Here the number of clusters(K) is a hyper-parameter and needs to be chosen very carefully. 
