# Python 3
# import simplejson as json
# import oauth2
import time
import json
import os
import requests
from datetime import datetime, date, timedelta

import gluon.contrib.simplejson as json
import oauth2

CONSUMER_KEY = '2972187968-JmUT3zeu2UyVIw315arct0tFjFO0J92r5ozwE1W'
CONSUMER_SECRET = 'FLqXC5f1UGUX4AwaKURWNDSUrB2FkRDajZemus9TKWhwY'
ACCESS_KEY = 'Z0ITlc1Fp5fAjZmX1ks8OzM2j'
ACCESS_SECRET = 'aLqR5uoV2vLLHCkIFmej3R43WGrqrfluZAguHuRRq0Xk8ScDBa'

def get_old_tweets():
    consumer = oauth2.Consumer(key=ACCESS_KEY, secret=ACCESS_SECRET)
    token = oauth2.Token(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    client = oauth2.Client(consumer, token)

    symbolList = ["LTC", "ETH", "XMR"]
    searchTermList = ['litecoin', 'ethereum', 'monero']

    for i in range(3):
        symbol = symbolList[i]
        searchTerm = searchTermList[i]
        url = "https://api.twitter.com/1.1/search/tweets.json?q="+searchTerm+"&result_type=recent&count=100&lang=en"
        page_count = 1
        max_page_count = 100
        attempt_count = 1
        max_attempt_count = 5
        breaker = False
        while((page_count <= max_page_count)&(attempt_count <= max_attempt_count)&(breaker == False)):
            time.sleep(5) # Set time lag
            resp, content = client.request(url, method="GET", headers=None)
            try:
                tweets = json.loads(content)
                next_results = tweets['search_metadata']['next_results']
                url = "https://api.twitter.com/1.1/search/tweets.json"+next_results

                tweet_statuses = tweets['statuses']
                for line in tweet_statuses:
                    if breaker == False and db(db.tweet.tweet_id == line['id']).select():
                        breaker = True

                    db.tweet.update_or_insert((db.tweet.tweet_id == line['id']),
                                              tweet_id = line['id'],
                                              coin_symbol = symbol,
                                              body = line['text'],
                                              created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(line['created_at'],'%a %b %d %H:%M:%S +0000 %Y')),
                                              retweet_count = line['retweet_count'],
                                              favorite_count = line['favorite_count'],
                                              user_id = line['user']['id'],
                                              user_followers_count = line['user']['followers_count'])
                    db.commit()

                page_count += 1
                attempt_count = 1
                print(symbol+str(page_count))
                print(url)
            except:
                attempt_count += 1

    get_current_price()
    get_tweet_sentiment()
    get_tweet_counts()
    return 'success'

def get_tweet_counts():
    nowDate = datetime.now().date()
    coin_history = db(db.coin_history.price_date == nowDate).select()
    for row in coin_history:
        coin_id = row.coin_id
        coin_symbol = db(db.master.id == coin_id).select().first().symbol
        date1 = datetime(row.price_date.year, row.price_date.month, row.price_date.day)
        date2 = date1 + timedelta(days=1)
        tweets = db((db.tweet.coin_symbol==coin_symbol)&(db.tweet.created_at >= date1)&(db.tweet.created_at < date2)).select()
        bullish_count, bearish_count, neutral_count = 0, 0, 0
        max_retweet_count = 0
        influential_tweet_id = 0
        influential_tweet_sentiment = 0
        for tweet in tweets:
            if tweet.sentiment != None:
                if tweet.user_followers_count > max_retweet_count:
                    influential_tweet_id = str(tweet.tweet_id)
                    influential_tweet_sentiment = tweet.sentiment
                    max_retweet_count = tweet.user_followers_count

                if tweet.sentiment == 1:
                    bullish_count += 1
                elif tweet.sentiment == -1:
                    bearish_count += 1
                else:
                    neutral_count += 1

        row.update_record(bullish_count=bullish_count, bearish_count=bearish_count, neutral_count=neutral_count, influential_tweet_id=influential_tweet_id, influential_tweet_sentiment=influential_tweet_sentiment)
        db.commit()
    return 'success'

def get_tweet_sentiment():
    tweets = db((db.tweet.sentiment==None)).select(orderby=~db.tweet.created_at)
    for tweet in tweets:
        sentiment = get_sentiment_results(tweet.body)
        if sentiment['prediction'] == 'Positive':
            tweet.update_record(sentiment=1)
        elif sentiment['prediction'] == 'Negative':
            tweet.update_record(sentiment=-1)
        else:
            tweet.update_record(sentiment=0)
        db.commit()
    return 'success'

def get_current_price():
    coin_id_list = [243, 2, 110]
    nowDate = datetime.now().date()
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum,litecoin,monero&vs_currencies=usd&include_24hr_change=false'
    priceList = json.loads(requests.get(url).content)
    price = priceList['ethereum']['usd']
    db.coin_history.update_or_insert((db.coin_history.coin_id==243)&(db.coin_history.price_date==nowDate), coin_id=243, price_date=nowDate, price_usd=price)
    price = priceList['litecoin']['usd']
    db.coin_history.update_or_insert((db.coin_history.coin_id==2)&(db.coin_history.price_date==nowDate), coin_id=2, price_date=nowDate, price_usd=price)
    price = priceList['monero']['usd']
    db.coin_history.update_or_insert((db.coin_history.coin_id==110)&(db.coin_history.price_date==nowDate), coin_id=110, price_date=nowDate, price_usd=price)
    return 'success'
