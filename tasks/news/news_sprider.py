# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: news_sprider
@time: 2018/3/26 下午5:22
"""
import time

from model.mongo import Mongo
from tasks.celery_app import celery_app
from tasks.news.data_util import get_cryptopanic
from tools.text_util import html2text


@celery_app.task
def cryptopanic_sprider():
    collection = Mongo().news
    news = get_cryptopanic()
    if not news:
        return False
    for new in news:
        source_id = new['pk']
        db_count = collection.find({
            'sprider_from': 'cryptopanic',
            'source_id': source_id
        }).count()
        if db_count > 0:
            continue
        insert_data = {
            'type': new['kind'],
            'created_at': int(time.time()),
            'author': new.get('domain'),
            'sprider_from': 'cryptopanic',
            'source': new['source']['domain'],
            'source_id': source_id,
            'title': new.get('title'),
            'content': html2text(new.get('body')),
            'url': new.get('url'),
            'images': new.get('image'),
            'has_keywords': 0,
            'has_send': 0,
            'repeat': -1
        }
        currencies = new.get('currencies')
        if currencies:
            for currencie in new['currencies']:
                insert_data.setdefault('keywords', []).append(currencie['code'])
            insert_data['has_keywords'] = 1
        collection.insert(insert_data)

if __name__ == '__main__':
    # cryptopanic_sprider()
    new = get_cryptopanic()