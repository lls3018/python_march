#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/5/8'


import time
from celery_app import app

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y