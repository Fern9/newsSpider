# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: text_util
@time: 2018/3/27 下午7:45
"""
from pyquery import PyQuery


def html2text(text):
    if not text:
        return ''
    dom = PyQuery(text)
    return dom.text()


if __name__ == '__main__':
    print(html2text(None))
