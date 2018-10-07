# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: celery_config
@time: 2018/2/26 上午12:04
"""
# from common import conf
from datetime import timedelta

BROKER_URL = 'redis://{}:{}'.format('127.0.0.1', '6400')  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://{}:{}/0'.format('127.0.0.1', '6400')  # 指定 Backend

CELERY_CREATE_MISSING_QUEUES = True  # 某个程序中出现的队列，在broker中不存在，则立刻创建它

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERYD_CONCURRENCY = 20  # 并发worker数

CELERY_ENABLE_UTC = False

CELERYD_FORCE_EXECV = True  # 强制退出

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_IGNORE_RESULT = True  # 忽略任务结果

CELERY_IMPORTS = (  # 指定导入的任务模块
    'tasks.github.spider',
    'tasks.twitter.spider',
    'tasks.bishijie.spider',
    'tasks.jinse.spider',
    'tasks.wallstreetcn.spider',
    'tasks.sync_data',
    'tasks.keywords.parse',
    'tasks.google_trends.spider',
    'tasks.sina.spider',
    'tasks.news_repeat.repeat',
    'tasks.news.news_spider',
    'tasks.hashbee_token.address',
    'tasks.hashbee_token.transaction'
)

CELERYBEAT_SCHEDULE = {
    'github_task': {
       'task': 'tasks.github.spider.start_spider',
       'schedule': timedelta(seconds=7200)
    },
    'twitter_user_task': {
       'task': 'tasks.twitter.spider.spider_user_info',
       'schedule': timedelta(seconds=7200)
    },
    # 'bishijie_task': {
    #    'task': 'tasks.bishijie.spider.start_spider',
    #    'schedule': timedelta(seconds=220)
    # },
    'jinse_task': {
       'task': 'tasks.jinse.spider.start_spider',
       'schedule': timedelta(seconds=200)
    },
    'cryptopanic_task': {
        'task': 'tasks.news.news_spider.cryptopanic_spider',
        'schedule': timedelta(seconds=300)
    },
    'wallstreetcn_task': {
       'task': 'tasks.wallstreetcn.spider.start_spider',
       'schedule': timedelta(seconds=200)
    },
    'sina_task': {
       'task': 'tasks.sina.spider.start_spider',
       'schedule': timedelta(seconds=200)
    },
    # 'google_trends_task': {
    #     'task': 'tasks.google_trends.spider.start_spider',
    #     'schedule': timedelta(seconds=20)
    # },
    'sync_news': {
       'task': 'tasks.sync_data.sync_news',
       'schedule': timedelta(seconds=120)
    },
    'sync_github': {
       'task': 'tasks.sync_data.sync_token_github',
       'schedule': timedelta(seconds=7200)
    },
    'sync_twitter': {
       'task': 'tasks.sync_data.sync_token_twitter',
       'schedule': timedelta(seconds=7200)
    },
    'sync_google_trends': {
       'task': 'tasks.sync_data.sync_google_trends',
       'schedule': timedelta(seconds=100)
    },
    'get_keywords': {
       'task': 'tasks.keywords.parse.deal_content',
       'schedule': timedelta(seconds=100)
    },
    'find_repeat_news': {
        'task': 'tasks.news_repeat.repeat.find_repeat_news',
        'schedule': timedelta(seconds=100)
    },
    'token_address': {
        'task': 'tasks.hashbee_token.address.get_token_address',
        'schedule': timedelta(seconds=1800)
    },
    'token_transaction': {
        'task': 'tasks.hashbee_token.transaction.get_transaction',
        'schedule': timedelta(seconds=300)
    },
    'sync_token_info': {
        'task': 'tasks.sync_data.send_token_info',
        'schedule': timedelta(seconds=200)
    }

}
