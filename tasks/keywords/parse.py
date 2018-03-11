# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: parse
@time: 2018/3/1 下午7:24
"""
from textrank4zh import TextRank4Keyword
from model.mongo import Mongo
from tasks.celery_app import celery_app

key_words = [
    'usdt',
    'ven',
    'veri',
    'waves',
    'wtc',
    'xlm',
    'xmr',
    'xrb',
    'xrp',
    'zec',
    'kcs',
    'lsk',
    'miota',
    'neo',
    'omg',
    'ppt',
    'sc',
    'steem',
    'strat',
    'ubtc',
    'gas',
    'dcr',
    'rep',
    'zrx',
    '0x',
    'ae',
    'bch',
    'dash',
    'ltc',
    'mkr',
    '狗狗币',
    'doge',
    'btc',
    'hsr',
    'kmd',
    'drgn',
    'ark',
    'ada',
    'ardr',
    'bcn',
    'bnb',
    'btg',
    'bts',
    'eos',
    'etc',
    'eth',
    'icx',
    'qtum',
    'snt',
    'trx',
    'xem',
    'xvg'
]


def get_keywords(text):
    result = []
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    for item in tr4w.get_keywords(20, word_min_len=2):
        result.append(item.word)
    return [_ for _ in result if _ in key_words]

@celery_app.task
def deal_content():
    collection = Mongo().news
    news = collection.find({
        'has_keywords': {
            '$ne': 1
        }
    })
    for new in news:
        if not new['title'] or not new['content']:
            continue
        text = new['title'] + ';' + new['content']
        keywords = get_keywords(text)
        new.update({
            'keywords': keywords,
            'has_keywords': 1
        })
        collection.save(new)

# deal_content()