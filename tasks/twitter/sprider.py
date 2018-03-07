# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/26 下午10:15
"""
import json

from tweepy import OAuthHandler, API, TweepError
import tweepy
from tasks.celery_app import celery_app
from model.mongo import Mongo

consumer_key = 'J9JdKy6PBwrWV61QdpvEHU0jx'
consumer_secret = 'tMDQagyWMiQVVz8dA9xEQP4qg30biFTQOzw3eJRtzE6KYGzrDU'
token_key = '968122104636891137-Vg05IKZVLEwIsGw9MUoJvwQIIoGTEKe'
token_secret = 'oReGfk7D9UwXOLbPbWUgqrh84XLu2KNj5XyoZ65S8oElR'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token_key, token_secret)
api = API(auth)
# api = API(auth, proxy='socks5://127.0.0.1:1086')
from common import get_tokens

# collection = Mongo().twitter


@celery_app.task
def get_user_info(token_name, username, token_id):
    try:
        collection = Mongo().twitter
        result = api.get_user(screen_name=username)
        result._json['token_name'] = token_name
        result._json['user_name'] = username
        result._json['token_id'] = token_id
        token = collection.find_one({"token_id": token_id, "user_name": username})
        if token:
            token.update(result._json)
            collection.save(token)
        else:
            collection.insert(result._json)
    except TweepError:
        pass


@celery_app.task
def sprider_user_info():
    tokens = get_tokens()
    for token in tokens:
        twitter = token.get('twitter_url')
        if not twitter or not twitter.strip():
            continue
        token_name = token['token_name']
        token_id = token['token_id']
        username = twitter.split('/')[-1]
        get_user_info.delay(token_name, username, token_id)


if __name__ == '__main__':
    # get_user_info('doge', 'DogeCoinShibe')
    sprider_user_info()
