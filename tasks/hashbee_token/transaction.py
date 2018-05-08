# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: transaction
@time: 2018/3/28 上午1:42
"""
import re
from time import mktime
import time
import datetime

from pyquery import PyQuery

from model.mongo import Mongo
from tasks.celery_app import celery_app
from tasks.keywords.parse import key_words


@celery_app.task
def get_transaction():
    collection = Mongo().token
    dom = PyQuery(url='http://www.blocktivity.info/')
    lists = dom('.font_size_row').items()
    for _ in lists:
        token_name = _('td').eq(2)('a').text().lower()
        print(token_name)
        transaction = _('td').eq(3).text()
        transaction = list(filter(str.isdigit, transaction))
        transaction = int(''.join(map(str, transaction)))
        print(transaction)
        db_result = collection.find_one({'token_name': token_name})
        if db_result:
            db_result.update({
                'transaction': transaction
            })
            collection.save(db_result)
        else:
            collection.insert({
                'token_name': token_name,
                'transaction': transaction
            })
    get_erc_transaction()


def get_erc_transaction():
    collection = Mongo().token
    p = 1
    # 取前面150位
    while p <= 3:
        list_page = PyQuery(url='https://etherscan.io/tokens')
        tokens = list_page('tbody')('tr').items()
        for token in tokens:
            token_name = token('h5')('a').text()
            token_name = re.findall(r'\w+', token_name)
            token_name = token_name[-1].lower()
            href = 'https://etherscan.io' + token('h5')('a').attr('href')
            contract_address = href.split('/')[-1]
            if token_name in key_words:
                try:
                    print(token_name)
                    transaction = get_single_erc_transaction(contract_address)
                    print(transaction)
                    db_result = collection.find_one({'token_name': token_name})
                    if db_result:
                        db_result.update({
                            'transaction': transaction
                        })
                        collection.save(db_result)
                    else:
                        collection.insert({
                            'token_name': token_name,
                            'transaction': transaction
                        })
                except:
                    print(contract_address)


def get_single_erc_transaction(contract_address):
    count = 1  # 计数用，防止迭代次数过多
    p = 51
    dom = PyQuery(
        'https://etherscan.io/token/generic-tokentxns2?contractAddress={}&mode=&p={}'.format(contract_address, p))
    time_str = dom('table')('tr').eq(1)('td').eq(1)('span').attr('title')
    delta_time = get_time(time_str)
    while count < 6 and (delta_time < 1420 or delta_time > 1460):
        count += 1
        p = int(1440.0 / delta_time * (p - 1)) + 1
        dom = PyQuery(
            'https://etherscan.io/token/generic-tokentxns2?contractAddress={}&mode=&p={}'.format(contract_address, p))
        time_str = dom('table')('tr').eq(1)('td').eq(1)('span').attr('title')
        delta_time = get_time(time_str)
        time.sleep(0.5)
    return int((p - 1) * 25 * (1440.0 / delta_time))


def get_time(time_str):
    date_time = datetime.datetime.strptime(time_str, '%b-%d-%Y %I:%M:%S %p')
    result = (mktime(datetime.datetime.now().timetuple()) - mktime(date_time.timetuple()) - 8 * 3600) / 60.0
    return result


# get_transaction()
# get_erc_transaction()
# get_time('May-08-2018 10:53:56 AM')
# print(get_single_erc_transaction('0xB8c77482e45F1F44dE1745F52C74426C631bDD52'))
get_erc_transaction()
