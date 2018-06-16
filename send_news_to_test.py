# -*- coding: utf-8 -*-
"""
@author: maozhufeng
@file: send_news_to_test
@time: 2018/6/16 下午12:41
"""
import pymongo
import requests

from common import conf
from model.mongo import Mongo

collection = Mongo().news
news_to_send = collection.find({
    'has_keywords': 1,
    'repeat': -1,
    'title': {'$ne': ''},
    'content': {'$ne': ''}
}).sort('created_at', pymongo.DESCENDING).limit(300)
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
        'keywords': new['keywords'],
        'keywordstext': ' '.join(new['keywords']) if new['keywords'] else '',
        'has_translated': str(new.get('has_translated', 0)),
        'translated_text': new.get('translated_text', ''),
        'translated_title': new.get('translated_title', '')
    })
# TODO test_environment
try:
    test_result = requests.post('http://47.52.103.240:18189' + conf['sync']['news_update'],
                  json={'batch_news': post_data})
    print('send news to test environment')
    print(post_data)
    print(test_result.json())
except:
    pass