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
- The number of dimentions in our vector-space must be chosen very carefully to prevent expensive and heavy calculations.
- Finding similar words for a given query word includes calculating similarity score(can be Euclidean Distance) between query word and all the words in our dictionary and is too expensive. Instead, the vectors(words) can be clustered using K-mean Clustering technic or Hierarchical clustering to present us with insights for discovering and visualizing groups of words which all are closely related. In the case of K-mean Clustering, first we need to calculate the distance between query word and the mean of each cluster and after finding the cluster of words which are closely realated to the query word, we need to calculate the similarity score only between query word and words contain in that cluster. Here the number of clusters(K) is a hyper-parameter and needs to be chosen very carefully.

## Entrepreneurial Thinking

My thoughts regarding questions, asked in the last part of the assignment, are as follow:
- One of the features that can be of much importance is: searching for talents by their images in desired webites to find all acounts, related to them. The other feature may be, giving recruiters the possibility to prioritize the desired skils for talents, they are searching for. The search engine can also be customized for each  user through learning from their clicks.
- For the case of searching with images, the desired platforms can be crawled for images and these images can be used to tag and prepare a dataset for training. The prioritization of skils(or any other features of importance) in a n-dimentional vector-space can be done through giving more weights to features that are desired. The data needed to actualize customized search engine can be obtained through monitoring and collecting user's clicks data from existing product.
- Here, the measure of success, as it is in the case of all data-driven online products, can be obtained and quantized through A/B testing of the new features. That means: The rise in number of users and their satisfaction by application of new features.
- For the purpose of searching by image, an object detection neural network can be very useful, specifically a YOLO v3 model, for its high obtainable accuracy and processing rate. For prioritization of features in our n-dimentional space, an unsupervied ranking model can be of use. In the case of customizing the search engine by learning through user's clicks, a simple multilayer feed forward perceptron network(MLP) can be trained to learn by giving it the query word, the search results presented to the user, and what the user decided to click. 
 
