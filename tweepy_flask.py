from flask import Flask, request, render_template
import tweepy
from flask import jsonify


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
    return render_template('tweepy.html')

@app.route('/tweets',methods = ['POST','GET'])
def tweepy_post():
    word = request.form['text']
    results = tweepy.Cursor(api.search, q=word,
                              count=200,
                              monitor_rate_limit=True, 
                              wait_on_rate_limit=True,
                              wait_on_rate_limit_notify = True,
                              retry_count = 5, 
                              retry_delay = 5,
                              lang = 'en').items(10)
    tweets = [item.text.strip() for item in results]
    return render_template('show_tweets.html',tweets = tweets)

if __name__ == "__main__":
    app.run(debug=True)