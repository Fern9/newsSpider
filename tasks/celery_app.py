# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: celery.app
@time: 2018/2/26 上午12:03
"""
from celery import Celery

# celery_app = Celery('hashbee_task', broker='redis://127.0.0.1:3999', include=['tasks.github.spider'])
celery_app = Celery('hashbee_task')
celery_app.config_from_object('tasks.celery_config')
