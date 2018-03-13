# -*- coding: utf-8 -*-
"""
@author: Fern9
@file: mail
@time: 2018/3/12 下午3:36
"""
import yagmail

yag = yagmail.SMTP(user='freya@wemart.cn', password='wwqiqi321', host='smtp.qq.com', port='465')
body = "喂喂喂"
result = yag.send(to='freya@wemart.cn', subject='工作文件', contents=[body])
print("已发送邮件")

