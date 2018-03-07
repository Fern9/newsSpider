# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: views
@time: 2018/2/26 下午4:03
"""
from flask import Blueprint, json

from model.mongo import Mongo
import pymongo
from tools import return_error, return_success

data_view = Blueprint('sprider', __name__)


@data_view.route('/github/<token_name>', methods=['GET'])
def get_github_data(token_name):
    collection = Mongo().github
    try:
        result = collection.find({'token_name': token_name}).sort('sprider_time', pymongo.DESCENDING).limit(1)[0]
        result.pop('_id')
        return return_success(data=result)
    except Exception as e:
        return return_error()


if __name__ == '__main__':
    get_github_data('dcr')
