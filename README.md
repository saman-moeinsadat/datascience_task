# Find similar words

## Setup:

This application uses GloVe pre-trained vectors and weights for the purpose of training a word to vector model. For downloading GloVe vectors please run this command: 
```
./setup.sh
```
Please note that running this command is necessary, only the first time deploying the docker container, afterwards the bash file checks for existence of GloVe model and if it exists, does not download the model again. 

## Serve application

For deploying the application locally please run this command: 
```
docker-compose up --build
```

Plaese note that this container includes three separate servies:
- train: Trains the model and pass the trained model to s3 bucket
- s3: Simple storage unit for uploading and downloading files between containers.
- app: Finds similar words for a given query word and check blocked and currated list for existence of the word.
