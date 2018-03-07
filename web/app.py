# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: app
@time: 2018/2/26 下午3:59
"""

from flask import Flask
from web.views import data_view

app = Flask(__name__)

app.register_blueprint(data_view, url_prefix='/data')

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
