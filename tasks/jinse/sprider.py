# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/28 下午6:01
"""
import time

import requests
from pyquery import PyQuery
from model.mongo import Mongo


from tasks.celery_app import celery_app


@celery_app.task
def start_sprider():
    collection = Mongo().news
    data = requests.get('https://api.jinse.com/v4/live/list?limit=20&reading=false')
    for date in data.json()['list']:
        for new in date['lives']:
            source_id = new['id']
            content = new['content']

            # 查询记录是否已经存在
            db_count = collection.find({
                'sprider_from': 'jinse',
                'source_id': source_id
            }).count()
            if db_count > 0:
                continue
            try:
                front_title_index = content.index('【')
                tail_title_index = content.index('】')
                title = content[front_title_index + 1: tail_title_index]
                content = content[tail_title_index + 1:]
            except Exception as e:
                title = ''
            insert_data = {
                'type': 'news',
                'created_at': int(time.time()),
                'author': "金色快讯",
                'sprider_from': 'jinse',
                'source': 'jinse',
                'source_id': source_id,
                'title': title,
                'content': content,
                'url': 'http://www.jinse.com/lives/' + str(source_id) + '.htm',
                'images': [],
                'keywords': [],
                'has_send': 0
            }
            collection.insert(insert_data)
    return True


if __name__ == '__main__':
    start_sprider()
