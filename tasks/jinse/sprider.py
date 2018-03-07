# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/28 下午6:01
"""
import time
from pyquery import PyQuery
from model.mongo import Mongo
from tasks.celery_app import celery_app


@celery_app.task
def start_sprider():
    collection = Mongo().news
    # html = requests.get('http://www.jinse.com/lives').text
    dom = PyQuery(url='http://www.jinse.com/lives')
    li_list = dom(".lost")("li")
    for li in li_list.items():
        source_id = li.attr("data-id")
        content = li(".live-info")('a').html()

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


