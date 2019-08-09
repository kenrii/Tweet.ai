from flask import Flask, request, render_template, json
import tweepy
from text_processing import text_manipulation
import pandas as pd
import collections
import itertools 

#Custom library for processing text
tp = text_manipulation()

#post request for tweepy api
app = Flask(__name__,template_folder='templates', static_folder='static')

consumer_key = 'IwpQtV35O2GKsiUaOxTkaNhE9'
consumer_key_secret = 'buKfFADTDoAmVBVhZu4l7gBWgs8z0vt15SwmrsHPeoV4qhMfh0'
access_token = '945059496631656448-8UeOdsnmF8htZ83KNqTZZ0LabXTarJJ'
access_token_secret = 'zj7XCAPEOEy8Ep6QhmbmidCgLXb0bqrbRKjW0B95Ubjal'
auth = tweepy.AppAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)
api = tweepy.API(auth)

@app.route('/')
def search_tweets():
    return render_template('index.html')

@app.route('/tweet_analysis',methods = ['POST','GET'])
def tweepy_post():
    word = request.form['text'] + '-filter:retweets'
    tweets = []
    for item in tweepy.Cursor(api.search, q=word, count=200, monitor_rate_limit=True, 
                              wait_on_rate_limit=True, wait_on_rate_limit_notify = True,
                              retry_count = 5, retry_delay = 5, tweet_mode = 'extended',
                              lang = 'en').items(1000):
        tweets.append(item.full_text)
    df_tweets = pd.DataFrame(tweets,columns=['tweet'])
    
    #processing data for sentimental analysis
    analysis_data = df_tweets['tweet'].apply(tp.preprocessing)
    results = tp.classify(analysis_data)
    results_json = json.dumps(results)

    #counting word occurrences for keyword data 
    keywords_data = analysis_data.str.split(expand=True).stack().value_counts()
    keywords_json = keywords_data.head(10).to_json() #top10 to json
    print(keywords_json)
    return render_template('tweet_analysis.html',tweets = results_json, keywords = keywords_json)

if __name__ == "__main__":
    app.run(debug=True)