# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sync_data
@time: 2018/2/27 下午6:16
"""
import json

import pymongo
import requests
from pymongo import MongoClient

from common import get_tokens, get_test_tokens
from model.mongo import Mongo
from common import conf
from tasks.celery_app import celery_app


@celery_app.task
def sync_token_github():
    tokens = get_tokens()
    for token in tokens:
        send_single_token_github(token['token_id'], token['ticker'].lower())
    sync_test_token_github()


@celery_app.task()
def send_single_token_github(token_id, token_name):
    collection = Mongo().github
    db_result = collection.find_one({
        'token_name': token_name,
    })
    if db_result:
        send_data = {
            "token_id": token_id,
            'url': db_result['github_url'],
            'star': db_result['star'],
            'fork': db_result['fork'],
            'user_count': db_result['watch'],
            'code_hot': db_result['star']
        }
        result = requests.post(conf['sync']['host'] + conf['sync']['git_update'], data=send_data)
        print(result.json())


def sync_test_token_github():
    tokens = get_test_tokens()
    collection = Mongo().github
    for token in tokens:
        db_result = collection.find_one({
            'token_name': token['ticker'].lower(),
        })
        if db_result:
            send_data = {
                "token_id": token['token_id'],
                'url': db_result['github_url'],
                'star': db_result['star'],
                'fork': db_result['fork'],
                'user_count': db_result['watch'],
                'code_hot': db_result['star']
            }
            print('send test environment github')
            print(send_data)
            result = requests.post('http://47.52.103.240:18189' + conf['sync']['git_update'], data=send_data)
            print(result.json())


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
        'repeat': -1,
        'title': {'$ne': ''},
        'content': {'$ne': ''}
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
            'spider_from': new['spider_from'],
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
    result = None
    try:
        result = requests.post(conf['sync']['host'] + conf['sync']['news_update'],
                               json={'batch_news': post_data})
        delete_repeat_news()
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
        news_send_finish(news_to_send)

    # TODO test_environment
    try:
        test_result = requests.post('http://47.52.103.240:18189' + conf['sync']['news_update'],
                                    json={'batch_news': post_data})
        print('send news to test environment')
        print(post_data)
        print(test_result.json())
        print('log_news_id', [_['new_id'] for _ in post_data])
    except:
        pass


@celery_app.task(bind=True)
def news_send_finish(self, news):
    try:
        collection = Mongo().news
        for new in news:
            new.update({
                'has_send': 1
            })
            collection.save(new)
    except:
        self.retry()


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


@celery_app.task
def send_token_info():
    collection = Mongo().token
    tokens = get_tokens()
    for token in tokens:
        token_name = token['ticker'].lower()
        db_result = collection.find_one({
            'token_name': token_name
        })
        if not db_result:
            continue
        data = {
            'token_id': token['token_id'],
            'transaction': db_result.get('transaction', 0),
            'holders': db_result.get('address', 0),
            'holders_increase': db_result.get('address_increase', 0)
        }
        try:
            result = requests.post(conf['sync']['host'] + conf['sync']['token_info'], data)
        except:
            pass
        # TODO test_environment
        send_test_token_info()


def send_test_token_info():
    collection = Mongo().token
    tokens = get_test_tokens()
    for token in tokens:
        token_name = token['ticker'].lower()
        db_result = collection.find_one({
            'token_name': token_name
        })
        if not db_result:
            continue
        data = {
            'token_id': token['token_id'],
            'transaction': db_result.get('transaction', 0),
            'holders': db_result.get('address', 0),
            'holders_increase': db_result.get('address_increase', 0)
        }
        try:
            result = requests.post('http://47.52.103.240:18189' + conf['sync']['token_info'], data)
        except:
            pass


def delete_repeat_news():
    collection = MongoClient('127.0.0.1', 27018).luckytoken.news
    news = collection.find({})
    useful = []
    _remove = []
    for new in news:
        if new['title'] in useful:
            _remove.append(new['title'])
            collection.remove(new)
        else:
            useful.append(new['title'])
    _remove = set(_remove)
    print('remove repeat {} news'.format(len(_remove)))


if __name__ == '__main__':
    # send_single_token_github(1671043044409346, 'dcr', 'https://github.com/decred/dcrd')
    # sync_news()
    # sync_google_trends()
    # sync_token_github()
    # send_token_info()
    # send_data = {
    #     "token_id": 1684300467602938,
    #     'url': 'test',
    #     'star': 1000,
    #     'fork': 1000,
    #     'user_count': 1000,
    #     'code_hot': 1000
    # }
    # result = requests.post('http://47.104.20.193:18189' + conf['sync']['git_update'], data=send_data)
    # print(result.json())
    # sync_test_token_github()
    # sync_token_github()
    # a = ['a', 'b']
    # a = None
    # print(' '.join(a))
    post_data = [{'new_id': '5b0cb99ecdc8723ec5f6daa5', 'type': 'news', 'author': '币世界', 'spider_from': 'bishijie',
                  'source': 'bishijie', 'title': '5月29日币市《板块风云榜》',
                  'content': '主力资金流向直接决定板块币种涨跌，《币世界》为您及时追踪主力资金意图，在繁多的板块币种里，挑选热门概念，规避冷门板块。欢迎阅读今日《板块风云榜》（附板块名单，点击”查看详情“）',
                  'url': 'http://www.bishijie.com/home/newsflashpc/detail?id=36988', 'created_at': 1527560449,
                  'images': [], 'keywords': [], 'has_translated': '0', 'translated_text': '', 'translated_title': ''},
                 {'new_id': '5b0cba7bcdc8723ec5f6db06', 'type': 'news', 'author': '币世界', 'spider_from': 'bishijie',
                  'source': 'bishijie', 'title': 'ONT官方twitter粉丝已超5万',
                  'content': '刚刚Ontology（ONT）官方发推称，开通twitter账号六个月以来粉丝已超5万。据《币世界》行情，ONT现均价5.73美元，跌幅11.39%。',
                  'url': 'http://www.bishijie.com/home/newsflashpc/detail?id=36989', 'created_at': 1527560784,
                  'images': [], 'keywords': ['eos'], 'keywordstext': 'eos', 'has_translated': '0',
                  'translated_text': '', 'translated_title': ''}]
    test_result = requests.post('http://47.52.103.240:18189' + conf['sync']['news_update'],
                                json={'batch_news': post_data})
    print('send news to test environment')
    print(post_data)
    print(test_result.json())
