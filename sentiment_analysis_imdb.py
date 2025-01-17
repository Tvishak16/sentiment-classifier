# -*- coding: utf-8 -*-
"""Sentiment_Analysis_IMDB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l2Ms5JPhqZSTLg5rUuRZHVztXoUD0tVj
"""

# Install downgraded version of numpy and restart the runtime otherwise you will get error "ValueError: Object arrays cannot be loaded when allow_pickle=False". 
# This issue is still up on keras git. I hope it gets solved as soon as possible
# pip install numpy==1.16.1

#Import Libraries
import numpy
from numpy import array
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Dropout
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.models import load_model
import re
import numpy as np
from nltk.tokenize import word_tokenize
import nltk

# fix random seed for reproducibility
numpy.random.seed(7)

# Load the dataset but only keep the top n words and zero out the rest i.e keep vocabulary size as 5000
top_words = 5000 #vocabulary_size = 5000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=top_words)

'''Inspect a sample review and its label.Note that the review is stored as a sequence of integers. These are word IDs that 
have been pre-assigned to individual words, and the label is an integer (0 for negative, 1 for positive).'''
print('---review---')
print(X_train[6])
print('---label---')
print(y_train[6])

'''We can use the dictionary returned by imdb.get_word_index() to map the review back to the original words.'''
word2id = imdb.get_word_index()
id2word = {i: word for word, i in word2id.items()}
print('---review with words---')
print([id2word.get(i, ' ') for i in X_train[6]])
print('---label---')
print(y_train[6])

print(word2id)

print(id2word)

#Maximum review length and minimum review length.
print('Maximum review length: {}'.format(
len(max((X_train + X_test), key=len))))

print('Minimum review length: {}'.format(
len(min((X_train + X_test), key=len))))

'''In order to feed this data into our RNN, all input documents must have the same length. We will limit the maximum review length to maximum words by truncating 
longer reviews and padding shorter reviews with a null value (0). We can accomplish this task using the pad_sequences() function in Keras. Here, setting max_review_length 
to 500.'''

max_review_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

'''Remember that our input is a sequence of words (technically, integer word IDs) of maximum length = max_review_length, and our output is a binary sentiment 
label (0 or 1).
'''
# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

'''We first need to compile our model by specifying the loss function and optimizer we want to use while training, as well as any evaluation metrics 
we’d like to measure. Specify the appropriate parameters, including at least one metric ‘accuracy’.'''
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=30, batch_size=64)

#Calculate Accuracy
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

#Run these codes first in order to install the necessary libraries and perform authorization

from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

#Mount your Google Drive:
!mkdir -p drive
!google-drive-ocamlfuse drive

#After success run Drive FUSE program, you can create a directory Sentiment_Analysis and access your drive at /content/drive with using command
import os
os.mkdir("/content/drive/Sentiment_Analysis")
os.chdir("/content/drive/")
!ls

#Append your path
import sys
sys.path.append('/content/drive/Sentiment_Analysis')

#Now save the model in required directory
model.save('/content/drive/Sentiment_Analysis/sentiment_analysis_model_new.h5')
print("Saved model to disk")

#Check the content of the directory
os.chdir("/content/drive/Sentiment_Analysis")
!ls

#Code to load the saved model
model = load_model('/content/drive/Sentiment_Analysis/sentiment_analysis_model_new.h5')
print("Model Loaded")





















