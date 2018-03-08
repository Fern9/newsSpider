# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/3/7 上午10:36
"""
import time
from pyquery import PyQuery

from model.mongo import Mongo
from tasks.celery_app import celery_app


@celery_app.task
def start_sprider():
    articles = PyQuery('http://tech.sina.com.cn/zt_d/qukuailiantk/')('.news-tit')
    for article in articles.items():
        url = article('a').attr('href')
        get_single_article(url)

def get_single_article(url):
    d = PyQuery(url=url, encoding="utf-8")
    a = d('#artibody')
    a.remove('#left_hzh_ad')
    content = a.text()
    title = d('.main-title').text()
    if not title:
        return False
    source = d('.source').text()
    collection = Mongo().news
    db_result = collection.find_one({
        'sprider_from': 'sina',
        'url': url
    })
    if db_result:
        return True
    insert_data = {
        'type': 'articles',
        'created_at': int(time.time()),
        'author': '',
        'sprider_from': 'sina',
        'source': source,
        'source_id': -1,
        'title': title,
        'content': content,
        'url': url,
        'images': [],
        'keywords': [],
        'has_send': 0
    }
    collection.insert(insert_data)
    return True


# start_sprider()
