# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sync_data
@time: 2018/2/27 下午6:16
"""
import json

import requests

from common import get_tokens
from model.mongo import Mongo
from common import conf
from tasks.celery_app import celery_app


@celery_app.task
def sync_token_github():
    collection = Mongo().github
    tokens = collection.find({})
    for token in tokens:
        send_single_token_github.delay(token['token_id'], token['token_name'], token['github_url'])


@celery_app.task()
def send_single_token_github(token_id, token_name, url):
    collection = Mongo().github
    db_result = collection.find_one({
        'token_name': token_name,
        'github_url': url
    })
    if db_result:
        send_data = {
            "token_id": token_id,
            'url': url,
            'star': db_result['star'],
            'fork': db_result['fork'],
            'user_count': db_result['watch'],
            'code_hot': db_result['star']
        }
        result = requests.post(conf['sync']['host'] + conf['sync']['git_update'], data=send_data)


@celery_app.task
def sync_token_twitter():
    collection = Mongo().twitter
    twitters = collection.find({})
    for twitter in twitters:
        sync_single_token_twitter.delay(twitter['token_id'], twitter['url'], twitter['followers_count'])


@celery_app.task
def sync_single_token_twitter(token_id, url, user_count):
    result = requests.post(conf['sync']['host'] + conf['sync']['twitter_update'], data={
        'token_id': token_id,
        'url': url,
        'user_count': user_count
    })


@celery_app.task(bind=True)
def sync_news(self):
    collection = Mongo().news
    news_to_send = collection.find({
        'has_send': 0,
        'has_keywords': 1,
        'repeat': -1
    }).limit(30)
    if news_to_send.count() == 0:
        return True
    news_to_send = list(news_to_send)
    news_to_send = [new for new in news_to_send if new['title'] is not None and new['content'] is not None]
    post_data = []
    for new in news_to_send:
        created_at = int(new['created_at'])
        if created_at < 10 ** 11:
            created_at *= 1000
        post_data.append({
            'new_id': str(new['_id']),
            'type': new['type'],
            'author': new['author'],
            'sprider_from': new['sprider_from'],
            'source': new['source'],
            'title': new['title'],
            'content': new['content'],
            'url': new['url'],
            'created_at': new['created_at'],
            'images': new['images'],
            'keywords': new['keywords']
        })
    result = None
    try:
        result = requests.post(conf['sync']['host'] + conf['sync']['news_update'],
                               json={'batch_news': post_data})
        print(result)
        result = result.json()
    except Exception as e:
        self.retry(e)
    if result['error_code'] == 0:
        for new in news_to_send:
            new.update({
                'has_send': 1
            })
            collection.save(new)


@celery_app.task
def sync_google_trends():
    collection = Mongo().google_trends
    trends = collection.find({})
    for trend in trends:
        if 'trends' not in trend or not trend['trends']:
            continue
        post_data = {
            'token_id': trend['token_id'],
            'search_number': trend['trends'][-1]['value'][0]
        }
        send_google_trend.delay(post_data)


@celery_app.task
def send_google_trend(data):
    try:
        result = requests.post(conf['sync']['host'] + conf['sync']['search_number_update'], json=data).json()
        print(result)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # send_single_token_github(1671043044409346, 'dcr', 'https://github.com/decred/dcrd')
    sync_news()
    # sync_google_trends()
    # sync_token_github()
