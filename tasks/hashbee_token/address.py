# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: address
@time: 2018/3/29 上午11:33
"""
import time

import pymongo
import requests
from pyquery import PyQuery
import re

from model.mongo import Mongo
from tasks.celery_app import celery_app
from tasks.keywords.parse import key_words
from common import get_tokens


def get_erc20():
    collection = Mongo().token_address
    p = 1
    # 取前面150位
    while p <= 3:
        list_page = PyQuery(url='https://etherscan.io/tokens')
        tokens = list_page('tbody')('tr').items()
        for token in tokens:
            token_name = token('h5')('a').text()
            token_name = re.findall(r'\w+', token_name)
            token_name = token_name[-1].lower()
            href = 'https://etherscan.io' + token('h5')('a').attr('href') + '#balances'
            if token_name in key_words:
                address = get_erc20_holders(href)
                collection.insert({
                    'token_name': token_name,
                    'address': address,
                    'time': int(time.time())
                })
            p += 1


def get_erc20_holders(url):
    page = PyQuery(url)
    holders = page('#ContentPlaceHolder1_divSummary')('tr').eq(3)('td').eq(1).text()
    result = re.findall(r'\d+', holders)
    if result:
        return int(result[0])
    return False


def get_btc_holders():
    collection = Mongo().token_address
    result = requests.get('https://api.blockchain.info/charts/my-wallet-n-users?format=json')
    if result.status_code == 200:
        values = result.json()['values']
        values = values[-5:-1]
        for value in values:
            db_result = collection.find_one({
                'token_name': 'btc',
                'time': value['x']
            })
            if not db_result:
                collection.insert({
                    'token_name': 'btc',
                    'time': value['x'],
                    'address': value['y']
                })


def get_eth_holders():
    collection = Mongo().token_address
    result = requests.get('https://etherscan.io/chart/address?output=csv')
    if result.status_code == 200:
        text = result.text
        values = text.split('\r\n')[-5:-1]
        for value in values:
            value = value.replace('"', '')
            value = value.split(',')
            address_time = int(value[1])
            address = int(value[2])
            db_result = collection.find_one({
                'token_name': 'eth',
                'time': address_time
            })
            if not db_result:
                collection.insert({
                    'token_name': 'eth',
                    'time': address_time,
                    'address': address
                })


def statistic_tokens_address():
    collection = Mongo().token
    tokens = get_tokens()
    for token in tokens:
        token_name = token['ticker'].lower()
        code, address, increase = statistic_token_address(token_name)
        if not code:
            address = 0
            increase = 0
        db_result = collection.find_one({'token_name': token_name})
        if db_result:
            db_result.update({
                'address': address,
                'address_increase': increase
            })
            collection.save(db_result)
        else:
            collection.insert({
                'token_name': token_name,
                'address': address,
                'address_increase': increase
            })


def statistic_token_address(token_name):
    collection = Mongo().token_address
    current_info = collection.find({
        'token_name': token_name
    }).sort('time', pymongo.DESCENDING).limit(1)
    if current_info.count() == 0:
        return False, False, False
    current_info = current_info[0]
    last_info = collection.find({
        'time': {'$gt': current_info['time'] - 86400},
        'token_name': token_name
    }).sort('time', pymongo.ASCENDING).limit(1)[0]
    if current_info['address'] - last_info['address'] == 0:
        last_info = collection.find({
            'time': {'$lte': current_info['time'] - 86400},
            'token_name': token_name
        }).sort('time', pymongo.DESCENDING).limit(1)[0]
    return True, current_info['address'], current_info['address'] - last_info['address']


@celery_app.task
def get_token_address():
    get_erc20()
    get_btc_holders()
    get_eth_holders()
    statistic_tokens_address()


if __name__ == '__main__':
    # get_erc20()
    # get_erc20_holders('https://etherscan.io/token/0xb64ef51c888972c908cfacf59b47c1afbc0ab8ac#balances')
    # get_btc_holders()
    # get_eth_holders()
    # statistic_token_address('bnb')
    statistic_tokens_address()
