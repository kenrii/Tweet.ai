from flask import Flask, request, render_template, json
import tweepy
from tweet_analysis import text_process
import pandas as pd
import collections

app = Flask(__name__, template_folder='templates', static_folder='static')

# Get personal keys and tokens from https://developer.twitter.com
consumer_key = #put it here
consumer_key_secret = #put it here
access_token = #put it here
access_token_secret = #put it here

auth = tweepy.AppAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


@app.route('/')
def search_tweets():
    return render_template('index.html')


@app.route('/results', methods=['POST', 'GET'])
def tweepy_post():
    tp = text_process()
    user_search = request.form['text'] + '-filter:retweets'
    searched_tweets = [tweet.full_text for tweet in tweepy.Cursor(
        api.search, q=user_search, count=200, monitor_rate_limit=True,
        retry_count=5, retry_delay=5, tweet_mode='extended', lang='en').items(1000)]
    df_tweets = pd.DataFrame(searched_tweets, columns=['tweet'])

    # Preprocessing and classifying tweets
    analysis_data = df_tweets['tweet'].apply(tp.preprocessing)
    results = tp.classify(analysis_data)
    results_json = json.dumps(results)

    # Counting word occurrences for tweets
    keywords_data = analysis_data.str.split(expand=True).stack().value_counts()
    keywords_json = keywords_data.head(10).to_json()
    return render_template('results.html', tweets=results_json, keywords=keywords_json)


if __name__ == "__main__":
    app.run(debug=True)
