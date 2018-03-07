# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/28 下午10:16
"""
import time
from pyquery import PyQuery
from model.mongo import Mongo
from tasks.celery_app import celery_app


@celery_app.task
def start_sprider():
    collection = Mongo().news
    # html = requests.get('http://www.jinse.com/lives').text
    dom = PyQuery(url='https://wallstreetcn.com/live/blockchain')
    pane = dom(".wscn-tab-pane")
    items = pane.items()
    next(items)
    pane = next(items)
    lives = pane('.live-item')
    for li in lives.items():
        source_id = None
        content = li('.live-item__main__content')('p').html()
        if not content:
            continue
        content_more = li('.live-item__main__content-more')('p').html()
        try:
            front_title_index = content.index('【')
            tail_title_index = content.index('】')
            title = content[front_title_index + 1: tail_title_index]
            content = content[tail_title_index + 1:]
        except Exception as e:
            title = ''
        if content_more:
            content += content_more

        images = []
        images_items = li('.live-item__main__images')('.zoomer__img')
        for image in images_items.items():
            images.append(image.attr('src'))
        # 查询记录是否已经存在
        db_count = collection.find({
            'sprider_from': 'wallstreetcn',
            'content': content
        }).count()
        if db_count > 0:
            continue

        insert_data = {
            'type': 'news',
            'created_at': int(time.time()),
            'author': "华尔街见闻",
            'sprider_from': 'wallstreetcn',
            'source': 'wallstreetcn',
            'source_id': -1,
            'title': title,
            'content': content,
            'url': '',
            'images': [],
            'keywords': [],
            'has_send': 0
        }
        collection.insert(insert_data)
    return True

# start_sprider()
