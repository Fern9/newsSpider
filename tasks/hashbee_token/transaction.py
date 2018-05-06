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

# get_transaction()
