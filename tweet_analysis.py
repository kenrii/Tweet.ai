import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize
import re
import string
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Download required nltk files
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
remove_emojis = re.compile('[^' + ''.join(string.printable) + ']')
remove_these = '[-()\"#/@;:<>{}`+=~|.!?,’\'&“”‘$£%_]|https?:\S+|http?:\S|@[\w]*'
custom_words = ['amp','like','one','two','would','also','say','thing','youu','youuu',"u'",'u',"u''", 'via']
stopwords = set(stopwords.words('english')).union(custom_words)

class text_process():

    def preprocessing(self, tweet):
        # Remove punctuations and unwanted text.
        tweet = re.sub(remove_these, ' ', tweet).lower()
        # Remove emojis
        tweet = remove_emojis.sub(' ', tweet)
        # Remove numbers
        tweet = re.sub('\d+', ' ', tweet)
        # Remove stopwords 
        tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
        # Tokenize tweet
        tweet = word_tokenize(tweet)
        # Lemmatize words
        tweet = [lemmatizer.lemmatize(w) for w in tweet]
        # Remove 'u'
        tweet = map(lambda item: item if item != 'u' else ' ', tweet)
        return ' '.join(tweet)
    
    def classify(self, tweet):
        # classify tweets with trained machine learning model
        ngram_vocabulary = pickle.load(open('model/ngram_vocabulary.pkl', 'rb'))
        ngram_vectorizer = CountVectorizer(vocabulary=ngram_vocabulary)
        X = ngram_vectorizer.transform(tweet)

        model = pickle.load(open('model/logreg_model.sav', 'rb'))
        prediction = list(model.predict(X))
        occurrences = [prediction.count(item) for item in set(prediction)]
        return occurrences


    

        
    
