#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/30'


def decorator(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


@decorator
def cnk(n,k):
    if k==0:
        return 1
    if n==0:
        return 0
    return cnk(n-1, k)+cnk(n-1, k-1)


print cnk(3,1)
