import json
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
import re
import string
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
remove_emojis = re.compile('[^' + ''.join(string.printable) + ']')
remove_these = '[-()\"#/@;:<>{}`+=~|.!?,’\'&“”‘$£%]|https?:\S+|http?:\S|[^A-Za-z0-9]+@[\w]*'
custom_words = ['amp','like','one','two','would','also','say','thing','youu','youuu',"u'",'u',"u''"]
stopwords = set(stopwords.words('english')).union(custom_words)

class text_manipulation():

    def preprocessing(self, tweet):
        # remove punctuations and unwanted text.
        tweet = re.sub(remove_these, ' ', tweet).lower()
        # remove emojis
        tweet = remove_emojis.sub(' ', tweet)
        # remove numbers
        tweet = re.sub('\d+', ' ', tweet)
        # remove stopwords 
        tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
        # tokenize tweets
        tweet = word_tokenize(tweet)
        #lemmatize tweets
        tweet = [lemmatizer.lemmatize(w) for w in tweet]
        #remove 'u'
        tweet = map(lambda item: item if item != 'u' else ' ', tweet)
        return ' '.join(tweet)
    
    def classify(self, tweet):
        #classify tweets
        ngram_vocabulary = pickle.load(open('model/ngram_vocabulary.pkl', 'rb'))
        ngram_vectorizer = CountVectorizer(vocabulary=ngram_vocabulary)
        X = ngram_vectorizer.transform(tweet)

        model = pickle.load(open('model/logreg_model.sav', 'rb'))
        prediction = list(model.predict(X))
        occurrences = [prediction.count(item) for item in set(prediction)]
        return occurrences


    

        
    
