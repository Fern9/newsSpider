# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: news_spider
@time: 2018/3/26 下午5:22
"""
import time

from pyquery import PyQuery

from model.mongo import Mongo
from tasks.celery_app import celery_app
from tasks.news.data_util import get_cryptopanic
from tools.text_util import html2text
from tools.translate import google_translate_list


@celery_app.task
def cryptopanic_spider():
    collection = Mongo().news
    news = get_cryptopanic()
    if not news:
        return False
    for new in news:
        source_id = new['pk']
        db_count = collection.find({
            'spider_from': 'cryptopanic',
            'source_id': source_id
        }).count()
        if db_count > 0:
            continue
        title, content = new.get('title'), html2text(new.get('body'))
        title_cn, content_cn = google_translate_list([title, content])
        insert_data = {
            'type': new['kind'],
            'created_at': int(time.time()),
            'author': new.get('domain'),
            'spider_from': 'cryptopanic',
            'source': new['source']['domain'],
            'source_id': source_id,
            'title': new.get('title'),
            'content': html2text(new.get('body')),
            'url': new.get('url'),
            'images': new.get('image'),
            'has_keywords': 0,
            'has_send': 0,
            'repeat': -1,
            'has_translated': 1,
            'translated_title': title_cn,
            'translated_text': content_cn
        }
        currencies = new.get('currencies')
        if currencies:
            for currencie in new['currencies']:
                insert_data.setdefault('keywords', []).append(currencie['code'])
            insert_data['has_keywords'] = 1
        collection.insert(insert_data)


def blockonomi_spider():
    dom = PyQuery(url='https://blockonomi.com/category/news/')
    news = dom('.grid-text').items()
    for new in news:
        title = new('.entry-title').text()
        url = new('.entry-title')('a').attr('href')
        content = new('p').text()
        print(title, url, content, '\n')


def smithandcrown_spider():
    dom = PyQuery(url='https://www.smithandcrown.com/research/')
    news = dom('article').items()
    for new in news:
        title = new('.is-size-5').text()
        content = new('.f-bodytext1').text()
        url = new('.is-size-5')('a').attr('href')
        print(title, url, content, '\n')

def trustnodes_spider():
    dom = PyQuery(url='https://www.trustnodes.com/news/news')
    news = dom('.news-details').items()
    for new in news:
        title = new('a').text()
        url = new('a').attr('href')
        new_dom = PyQuery(url=url)
        content = new_dom('.post-content')('p').eq(0).text()


if __name__ == '__main__':
    # cryptopanic_spider()
    # new = get_cryptopanic()
    # blockonomi_spider()
    # smithandcrown_spider()
    trustnodes_spider()