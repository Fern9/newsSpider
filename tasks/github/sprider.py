# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: sprider
@time: 2018/2/26 上午12:15
"""
import requests
import time

from model.mongo import Mongo
from tasks.celery_app import celery_app
from common import get_tokens
from tasks.sprider_config import github_api_host


class GithubSpider():
    def __init__(self):
        self.collection = Mongo().github

    @staticmethod
    @celery_app.task
    def get_data(token_name, url, api_url, token_id):
        collection = Mongo().github
        result = requests.get('{}?client_id={}&client_secret={}'.format(api_url, 'dcc3734066251548c999', '89d90ad41f32b18d2ed689cb21875b75e88a2d82')).json()
        if 'forks_count' not in result:
            # TODO record error result
            return
        token = collection.find_one({
            'token_name': token_name,
            'github_url': url
        })
        insert_data = {
            'token_name': token_name,
            'github_url': url,
            'token_id': token_id,
            'star': result['stargazers_count'],
            'fork': result['forks_count'],
            'watch': result['subscribers_count'],
            'sprider_time': time.time(),
            'update_time': result['updated_at'],
            'create_time': result['created_at']
        }
        if token:
            token.update(insert_data)
            collection.save(token)
        else:
            collection.insert(insert_data)

    @staticmethod
    @celery_app.task
    def start_sprider():
        tokens = get_tokens()
        for token in tokens:
            github_url = token.get('github_url')
            if not github_url or not github_url.strip():
                continue
            github_url = github_url.strip('/')
            repo = github_url.split('/')[-2] + '/' + github_url.split('/')[-1]
            GithubSpider.get_data(token['ticker'].lower(), github_url, github_api_host + repo, token['token_id'])


if __name__ == '__main__':
    GithubSpider().start_sprider()
