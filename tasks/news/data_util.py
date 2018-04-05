# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: data
@time: 2018/3/27 下午2:18
"""
import base64
import json

import requests

import zlib
from Crypto.Cipher import AES


def get_cryptopanic():
    try:
        csrftoken = 'MrNEPeRpvcD2YdnnMkr2iCMBDRxOuNETZShuvC0NvrH2neRCEQfnAoHWjUX8NiDg'
        cookies = {
            'sessionid': '1aqc3cqcll75878v6ngoma22zibtxjg8',
            'csrftoken': csrftoken,
            'AWSALB': '+uDisszkxIGWY1R1t0q5kQVx2tcl2NR0ZUTEm6TDZtd6PaElSOdEr/DUTHWGQFlAQmWAV8Bers6h5eNeobr6W1vDMRacRK9+Rvd8gdOv/sI4/ZDVDEtsYZlHqUuC',
            '_gid': 'GA1.2.1644343046.1522051680',
            '_ga': 'GA1.2.475994179.1520255898'
        }

        headers = {
            # ':authority': 'cryptopanic.com',
            # ':method': 'POST',
            # ':path': '/web-api/posts/',
            # ':scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': '167',
            # 'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarynZn8qg61dnCGrBLT',
            'origin': 'https://cryptopanic.com',
            'pragma': 'no-cache',
            'referer': 'https://cryptopanic.com/news/1479073/Sierra-Leone-What-We-Got-Wrong',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'x-csrftoken': csrftoken,
            'x-requested-with': 'XMLHttpRequest',
        }

        files = {"filters": (None, '{"page":0}')}

        result = requests.post('https://cryptopanic.com/web-api/posts/', cookies=cookies, headers=headers, files=files)
        origin_text = result.json()['s']
        debase64 = base64.b64decode(origin_text)

        password = u')b7Z*$+)/T}$9>/L'
        iv_pass = u'MrNEPeRpvcD2Ydnn'
        obj = AES.new(password, AES.MODE_CBC, iv_pass)
        # 解密
        buff = obj.decrypt(debase64)

        buff = zlib.decompress(buff)
        result = json.loads(buff)
        news = []
        for new in result['l']:
            news.append(dict(zip(result['k'], new)))
        return news
    except:
        return []
