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
    'tasks.github.sprider',
    'tasks.twitter.sprider',
    'tasks.bishijie.sprider',
    'tasks.jinse.sprider',
    'tasks.wallstreetcn.sprider',
    'tasks.sync_data',
    'tasks.keywords.parse'
)

CELERYBEAT_SCHEDULE = {
    'github_task': {
        'task': 'tasks.github.sprider.start_sprider',
        'schedule': timedelta(seconds=7200)
    },
    'twitter_user_task': {
        'task': 'tasks.twitter.sprider.sprider_user_info',
        'schedule': timedelta(seconds=7200)
    },
    'bishijie_task': {
        'task': 'tasks.bishijie.sprider.start_sprider',
        'schedule': timedelta(seconds=300)
    },
    'jinse_task': {
        'task': 'tasks.jinse.sprider.start_sprider',
        'schedule': timedelta(seconds=300)
    },
    'wallstreetcn_task': {
        'task': 'tasks.wallstreetcn.sprider.start_sprider',
        'schedule': timedelta(seconds=300)
    },
    'sync_news': {
        'task': 'tasks.sync_data.sync_news',
        'schedule': timedelta(seconds=60)
    },
    'get_keywords': {
        'task': 'tasks.keywords.parse.deal_content',
        'schedule': timedelta(seconds=60)
    }
}
