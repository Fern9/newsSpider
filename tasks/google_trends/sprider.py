# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/3/2 下午10:40
"""
import socket
import socks
import requests
import json
from common import get_tokens
from model.mongo import Mongo
from tasks.celery_app import celery_app

@celery_app.task
def get_google_trend(key, token_id):
    # socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
    temp_socket = socket.socket
    socket.socket = socks.socksocket
    token, search_time = get_google_token(key)
    headers = {
        'host': 'trends.google.com',
        'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Referfer': 'https://trends.google.com/trends/explore?q=' + key,
        'x-client-data': 'CJa2yQEIo7bJAQjBtskBCKmdygEIqKPKAQ=='
    }
    request_url = 'https://trends.google.com/trends/api/widgetdata/multiline?hl=zh-CN&tz=-480&req=%7B%22time%22:%22{}%22,%22resolution%22:%22DAY%22,%22locale%22:%22zh-CN%22,%22comparisonItem%22:%5B%7B%22geo%22:%7B%7D,%22complexKeywordsRestriction%22:%7B%22keyword%22:%5B%7B%22type%22:%22BROAD%22,%22value%22:%22{}%22%7D%5D%7D%7D%5D,%22requestOptions%22:%7B%22property%22:%22%22,%22backend%22:%22IZG%22,%22category%22:0%7D%7D&token={}&tz=-480'.format(
        search_time, key, token)
    result = requests.get(request_url, headers=headers).text[5:]
    result = json.loads(result)
    data = result['default']['timelineData']
    socket.socket = temp_socket
    collection = Mongo().google_trends
    collection.insert({
        'token_id': token_id,
        'token_name': key,
        'trends': data
    })
    return True


def get_google_token(key):
    headers = {
        'host': 'trends.google.com',
        'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Referfer': 'https://trends.google.com/trends/explore?q='+key,
        'x-client-data': 'CJa2yQEIo7bJAQjBtskBCKmdygEIqKPKAQ=='
    }
    request_url = 'https://trends.google.com/trends/api/explore?hl=zh-CN&tz=-480&req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22{}%22,%22geo%22:%22%22,%22time%22:%22today+3-m%22%7D%5D,%22category%22:0,%22property%22:%22%22%7D&tz=-480'.format(
        key)
    result = requests.get(request_url, headers=headers).text[5:]
    result = json.loads(result)
    token = result['widgets'][0]['token']
    search_time = result['widgets'][0]['request']['time']
    return token, search_time

@celery_app.task
def start_sprider():
    tokens = get_tokens()
    for token in tokens:
        get_google_trend.delay(token['name'], token['token_id'])

if __name__ == '__main__':
    start_sprider()
