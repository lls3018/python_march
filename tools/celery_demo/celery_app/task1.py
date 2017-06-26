#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/5/8'


import time
from celery_app import app

@app.task
def add(x, y):
    time.sleep(2)     # 模拟耗时操作
    return x + y