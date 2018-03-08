# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/3/7 上午10:36
"""

from pyquery import PyQuery


def start_sprider():
    articles = PyQuery('http://tech.sina.com.cn/zt_d/qukuailiantk/')('.news-tit')
    for article in articles.items():
        print(article('a').attr('href'))


def get_single_article(url):
    d = PyQuery(url='http://tech.sina.com.cn/i/2018-03-04/doc-ifwnpcnt8149255.shtml', encoding="utf-8")
    a = d('#artibody')
    a.remove('#left_hzh_ad')
    text = a.text()


start_sprider()
