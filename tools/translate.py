# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: translate
@time: 2018/3/27 下午7:12
"""
import requests


def google_translate_list(texts, target='zh-CN'):
    count = 0
    while count <=3:
        url = 'https://translation.googleapis.com/language/translate/v2?key=AIzaSyBCtkbafEHIG1ZPwSaCVda228KWnIfU1-s'
        data = [('target', target)]
        for text in texts:
            data.append(('q', text))
        data = tuple(data)
        result = requests.post(url, data=data)
        if result.status_code == 200:
            return [_['translatedText'] for _ in result.json()['data']['translations']]
        else:
            count += 1
    return False


def google_translate(text, target='zh-CN'):
    count = 0
    while count <= 3:
        url = 'https://translation.googleapis.com/language/translate/v2?key=AIzaSyBCtkbafEHIG1ZPwSaCVda228KWnIfU1-s'
        data = (('target', target), ('q', text))
        result = requests.post(url, data=data)
        if result.status_code == 200:
            print(result.json())
            return result.json()['data']['translations'][0]['translatedText']
        else:
            count += 1
    return False


if __name__ == '__main__':
    print(google_translate_list(['hello world', 'where are you', 'hello world']))
    # print(google_translate('hello world'))
