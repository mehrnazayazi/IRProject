
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



def RecievTweets(tweets):
    # twitter_users.append(None)

    for i in range(2):
        # print(i)
        # print(twitter_users)
        for tweet in Cursor(twitter_client.user_timeline, id=twitter_users1[i]).items(1):
            fileName = "tweet" + str(tweet.id)+".json"
            tweets.append(tweet)
            df = pd.DataFrame(data=[tweet.text], columns=['Tweets'])
            df['id'] = np.array([tweet.id])
            df['Username'] = np.array([tweet.screen_name])
            df['len'] = np.array([len(tweet.text)])
            df['date'] = np.array([tweet.created_at])
            df['source'] = np.array([tweet.source])
            df['likes'] = np.array([tweet.favorite_count])
            df['retweets'] = np.array([tweet.retweet_count])
            # json_dict = json.loads(df.to_json(orient='split'))
            # del json_dict['index']
            # with open(fileName, 'w') as outfile:
            #     json.dump(json_dict, outfile)
            print(df.reset_index().to_json(orient='records'))
            df.to_json(orient='records', path_or_buf=fileName)
        print("len tweets = ")
        print(len(tweets))
        # print(twitter_users[i])
        for friend in twitter_client.friends(twitter_users1[i]):
            twitter_users1.append(friend.screen_name)
    return


# print(tweets)


def tweets_to_data_frame(tweets):
    df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

    df['id'] = np.array([tweet.id for tweet in tweets])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['date'] = np.array([tweet.created_at for tweet in tweets])
    df['source'] = np.array([tweet.source for tweet in tweets])
    df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

    return df



RecievTweets(tweets)


# _thread.start_new_thread(RecievTweets, (tweets,))
# tweetsDf = tweets_to_data_frame(tweets)
# tweetsDf.to_json(r'tweets.json')
# print(tweetsDf)



