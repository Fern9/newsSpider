# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/27 下午4:20
"""
import requests
from tasks.celery_app import celery_app
from model.mongo import Mongo
from common import conf


@celery_app.task(bind=True)
def start_sprider(self):
    result = None
    try:
        result = requests.get(conf['news']['bishijie']).json()
        collection = Mongo().news
        if result['error'] != 0:
            self.retry()
        result = result['data']
        for date in result:
            id_list = [new['newsflash_id'] for new in result[date]['buttom']]
            db_news = collection.find({
                    'sprider_from': 'bishijie',
                    'source_id': {'$in': id_list}
                })
            db_id_list = [new['source_id'] for new in db_news]
            for new in result[date]['buttom']:
                if new['newsflash_id'] in db_id_list:
                    continue
                content = new['content']
                try:
                    front_title_index = content.index('【')
                    tail_title_index = content.index('】')
                    title = content[front_title_index + 1: tail_title_index]
                    content = content[tail_title_index + 1:]
                except Exception as e:
                    title = ''
                insert_data = {
                    'type': 'news',
                    'created_at': new['issue_time'],
                    'author': new['source'],
                    'sprider_from': 'bishijie',
                    'source': 'bishijie',
                    'source_id': new['newsflash_id'],
                    'title': title,
                    'content': content,
                    'url': 'http://www.bishijie.com/home/newsflashpc/detail?id=' + str(new['newsflash_id']),
                    'images': [],
                    'keywords': [],
                    'has_send': 0
                }
                collection.insert(insert_data)
    except Exception as e:
        self.retry(e)

start_sprider()
