# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/3/7 上午10:36
"""

from pyquery import PyQuery

d = PyQuery(url='http://tech.sina.com.cn/i/2018-03-04/doc-ifwnpcnt8149255.shtml')
a = d('.article-content-left')
print(a.html())