# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: address
@time: 2018/3/29 上午11:33
"""
import time

import requests
from pyquery import PyQuery
import re

from model.mongo import Mongo
from tasks.keywords.parse import key_words


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


if __name__ == '__main__':
    # get_erc20()
    # get_erc20_holders('https://etherscan.io/token/0xb64ef51c888972c908cfacf59b47c1afbc0ab8ac#balances')
    # get_btc_holders()
    get_eth_holders()
