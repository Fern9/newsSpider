# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: mongo
@time: 2018/2/26 上午1:30
"""
from pymongo import MongoClient
from common import conf

class Mongo():

    db = None

    def __new__(cls, *args, **kwargs):
        # if cls.db is None:
        cls.db = MongoClient(conf['mongo']['host'], int(conf['mongo']['port'])).sprider
        return cls.db



