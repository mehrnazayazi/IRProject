
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

import numpy as np
import pandas as pd
import _thread
import time
import json


auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
twitter_client = API(auth)
twitter_user = "PatMcAfeeShow"


def get_friend_list(twitter_user):
    friend_list = []
    for friend in Cursor(twitter_client.friends, id=twitter_user).items(2):
        friend_list.append(friend)
    return friend_list


tweets = []
twitter_users1 = []
twitter_users1.append("PatMcAfeeShow")
checked_tweets = []
checked_users = []


def recievTweets(tweets):
    for i in range(100):
        for tweet in Cursor(twitter_client.user_timeline, id=twitter_users1[i], count=5).items():
            try:
                if checked_tweets.__contains__(tweet.id):
                    break
                checked_tweets.append(tweet.id)
                fileName = "./Data/tweet" + str(tweet.id)+".json"
                tweets.append(tweet)
                df = tweets_to_data_frame(tweet)
                df.to_json(orient='records', path_or_buf=fileName)
            except:
                continue
        for friend in twitter_client.friends(twitter_users1[i]):
            if checked_users.__contains__(friend):
                continue
            else:
                twitter_users1.append(friend.screen_name)
    return




def tweets_to_data_frame(tweet):
    df = pd.DataFrame(data=[tweet.text], columns=['Tweets'])
    df = pd.DataFrame(data=[tweet.text], columns=['tweets'])
    df['id'] = np.array([tweet.id])
    df['screen_name'] = np.array([tweet.user.screen_name])
    df['name'] = np.array([tweet.user.name])
    df['location'] = np.array([tweet.user.location])
    df['description'] = np.array([tweet.user.description])
    df['followers_count'] = np.array([tweet.user.followers_count])
    df['len'] = np.array([len(tweet.text)])
    df['date'] = np.array([tweet.created_at])
    df['source'] = np.array([tweet.source])
    df['likes'] = np.array([tweet.favorite_count])
    df['retweets'] = np.array([tweet.retweet_count])
    return df


if __name__ == '__main__':
    recievTweets(tweets)


# _thread.start_new_thread(RecievTweets, (tweets,))
# tweetsDf = tweets_to_data_frame(tweets)
# tweetsDf.to_json(r'tweets.json')
# print(tweetsDf)



