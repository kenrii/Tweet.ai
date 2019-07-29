import json
import pandas as pd
import numpy as np
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
from textblob import Word
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
remove_these = '@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+@[\w]*'
stopwords = set(stopwords.words('english'))

class text_manipulation():

    def convert_json(self, json_data):
        #convert json to dataframe
        data = [item.text.strip() for item in json_data]
        print(data)
        return pd.DataFrame(data)

    def cleaning(self, tweet):
        #lemmatize, remove stopwords and other not important syntax
        tokens = []
        tweet = re.sub(remove_these,' ',str(tweet).lower()).strip()
        tweet_tokenized = word_tokenize(tweet)
        tweet = [word for word in tweet_tokenized if word not in stopwords] #stopwordid
        tweet = [Word(w).lemmatize() for w in tweet]
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


    

        
    
