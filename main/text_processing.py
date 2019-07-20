import json
import pandas as pd

import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
from textblob import Word
import re

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
        

    

        
    
