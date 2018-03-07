# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: tools
@time: 2018/2/26 下午5:55
"""
from flask import json


def return_success(code=0, msg='success', data=[]):
    return json.dumps({
        'code': code,
        'msg': msg,
        'data': data
    })


def return_error(code=-1, msg='failed', data=[]):
    return json.dumps({
        'code': code,
        'msg': msg,
        'data': data
    })
