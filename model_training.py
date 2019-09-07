import pandas as pd
import pickle
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tweet_analysis import text_process

file_path = 'polarity_data_twitter.csv' # Path to your file that contains data for model training
polarity_column = 'polarity'  # Name of a column that contains negative, neutral and positive polarity values
tweets_column = 'tweet'  # Name of a column that contains rows of tweets
col_fields = [polarity_column, tweets_column]
data = pd.read_csv(file_path, usecols=col_fields)

tp = text_process()
preprocessed_tweets = data[tweets_column].apply(tp.preprocessing)
le = preprocessing.LabelEncoder()
labels = le.fit_transform(data[polarity_column])

X_train, X_test, y_train, y_test = train_test_split(
    preprocessed_tweets, labels, train_size=0.9,
    stratify=labels, random_state=42)
ngram_vectorizer = CountVectorizer()
X_train = ngram_vectorizer.fit_transform(X_train)
X_test = ngram_vectorizer.transform(X_test)

model = LogisticRegression(C=0.1, multi_class='multinomial', solver='lbfgs')
model.fit(X_train, y_train)
predictions = model.predict(X_test)
model_accuracy = accuracy_score(y_test, predictions)

print('Model accuracy is {:.1%}.'.format(round(model_accuracy, 3)))
print('Do you want to save the model and ngram vocabulary?')
answer = input('YES: type "y" and press enter || NO: type anything else and press enter \n')
if answer == 'y':
    pickle.dump(model, open('model.sav', 'wb'))
    pickle.dump(ngram_vectorizer.vocabulary_, open('vocabulary.pkl', 'wb'))
    print('Model and vocabulary saved.')
else:
    print('Model and vocabulary discarded.')
