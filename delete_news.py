# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: delete_news
@time: 2018/4/10 上午12:11
"""
from __future__ import absolute_import
import sys
from pymongo import MongoClient

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

useful = set(useful)
_remove = set(_remove)
print(len(_remove), len(useful), len([_ for _ in _remove if _ in useful]))
