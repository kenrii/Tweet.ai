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
custom_words = ['amp', 'like', 'one', 'two', 'would', 'also', 'say', 'thing', 'u', 'via']
stopwords = set(stopwords.words('english')).union(custom_words)


class text_process:
    def preprocessing(self, tweet):
        """ Removes punctuations, emojis, numbers and nltk stopwords.

        Returns lemmatized tweet in string form.
        """
        tweet = re.sub(remove_these, ' ', tweet).lower()
        tweet = remove_emojis.sub(' ', tweet)
        tweet = re.sub('\d+', ' ', tweet)
        tweet = ' '.join([word for word in tweet.split() if word not in stopwords])
        tweet = word_tokenize(tweet)
        tweet = [lemmatizer.lemmatize(w) for w in tweet]
        tweet = map(lambda item: item if item != ('u' and 'string') else ' ', tweet)

        return ' '.join(tweet)

    def classify(self, tweet):
        """Classify tweet data with trained machine learning model.

        Returns a list of integers that represent numbers of positive, neutral and negative tweets.
        """
        ngram_vocabulary = pickle.load(open('model/ngram_vocabulary.pkl', 'rb'))
        ngram_vectorizer = CountVectorizer(vocabulary=ngram_vocabulary)
        vectorized_data = ngram_vectorizer.transform(tweet)

        model = pickle.load(open('model/logreg_model.sav', 'rb'))
        model_predictions = list(model.predict(vectorized_data))
        polarity_occurrences = [model_predictions.count(item) for item in set(model_predictions)]

        return polarity_occurrences
