# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: common
@time: 2018/2/27 下午6:36
"""
import json
import urllib

import requests
import configparser

conf = configparser.ConfigParser()
conf.read('/opt/hashbee/sprider_setting.conf')


# class Configer():
#     def __init__(self):
#         self.conf = configparser.ConfigParser()
#         self.conf.read('/opt/hashbee/setting.conf')
#
#     def get(self, section, key):
#         return self.conf[section][key]


def get_tokens():
    try:
        result = requests.post(conf['sync']['host'] + conf['sync']['address_list']).json()
        print(result)
        if result['error_code'] != 0:
            return False
        return result['result']
    except Exception as e:
        return False


def get_test_tokens():
    try:
        result = requests.post('http://47.104.20.193:18189' + conf['sync']['address_list']).json()
        print(result)
        if result['error_code'] != 0:
            return False
        return result['result']
    except Exception as e:
        return False


if __name__ == '__main__':
    print(get_tokens())
