# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: delete_news
@time: 2018/4/10 上午12:11
"""
from __future__ import absolute_import
import sys
print(sys.path)
from pymongo import MongoClient
from html.parser import HTMLParser

collection = MongoClient('127.0.0.1', 27018).luckytoken.news

html_parser = HTMLParser()
news = collection.find({})
for new in news:
        if 'translated_title' in new:
            new['translated_title'] = html_parser.unescape(new['translated_title'])
            new['translated_text'] = html_parser.unescape(new.get('translated_text', ''))
            collection.save(new)

