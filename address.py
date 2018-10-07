# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: address
@time: 2018/8/19 下午10:11
"""
import socket

import socks
import time
from pyquery import PyQuery
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1086)
temp_socket = socket.socket
socket.socket = socks.socksocket


headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'cookie': 'aQQ_ajkguid=7547DC39-FA08-848B-5F27-2286FD9AEFEB; lps=http%3A%2F%2Fwww.anjuke.com%2F%7Chttps%3A%2F%2Fwww.google.com%2F; ctid=11; twe=2; sessid=2991936F-9AA8-32D2-D44A-47584916F057; 58tj_uuid=f69cd5d1-c50a-475b-b303-cca75fa5bade; init_refer=https%253A%252F%252Fwww.google.com%252F; new_uv=1; wmda_uuid=fe91427d40ad3e0fb11f9c657153a7d4; wmda_new_uuid=1; wmda_session_id_6289197098934=1534689355009-d0099026-f179-d69b; wmda_visited_projects=%3B6289197098934; __xsptplusUT_8=1; als=0; new_session=0; _ga=GA1.2.554880405.1534689375; _gid=GA1.2.1463375495.1534689375; __xsptplus8=8.1.1534689355.1534689391.5%233%7Cwww.google.com%7C%7C%7C%7C%23%23iADUpNqPPw67vn1NZyVj384MVYkRdqEd%23; search_words=%E8%BE%BD%E6%BA%90%E5%9B%9B%E6%9D%91',
    'pragma': 'no-cache',
    'referer': 'https://shanghai.anjuke.com/sale/rd1/?from=zjsr&kw=%E8%BE%BD%E6%BA%90%E5%9B%9B%E6%9D%91',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

with open('/Users/mzfenng/work/lsy/address', encoding='utf8') as data:
    for name in data.readlines():
        name = name.replace('\n', '')
        dom = PyQuery(url='https://shanghai.anjuke.com/community/?kw={}&from=sugg_hot'.format(name), headers=headers)
        name1 = dom('.list-content')('.li-itemmod').eq(0)('h3')('a').text()
        price = dom('.list-content')('.li-itemmod').eq(0)('.li-side')('strong').text()
        print(name, name1, price)
        time.sleep(2)
