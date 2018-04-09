# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: transaction
@time: 2018/3/28 上午1:42
"""

from pyquery import PyQuery

from model.mongo import Mongo
from tasks.celery_app import celery_app
from tasks.keywords.parse import key_words


@celery_app.task
def get_transaction():
    dom = PyQuery(url='http://www.bishijie.com/hangqing/coins/top/200')
    lists = dom('#table_body')('tr').items()
    collection = Mongo().token
    for _ in lists:
        token_name = _.attr('data-slug').split('-')[-1]
        if token_name in key_words:
            db_result = collection.find_one({'token_name': token_name})
            if db_result:
                db_result.update({
                    'transaction': _('.volume').attr('data-usd')
                })
                collection.save(db_result)
            else:
                collection.insert({
                    'token_name': token_name,
                    'transaction': _('.volume').attr('data-usd')
                })


# get_transaction()
