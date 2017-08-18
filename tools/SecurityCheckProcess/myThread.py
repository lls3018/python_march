#!/usr/bin/python
#coding=utf-8

import threading
import time


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def getResult(self):
        return self.res

    def run(self):
        print 'starting %s at:%s' % (self.name, time.strftime('%Y-%m-%d %H:%M:%S'))
        self.res = apply(self.func, self.args)
        print '%s finished at:%s' % (self.name, time.strftime('%Y-%m-%d %H:%M:%S'))
