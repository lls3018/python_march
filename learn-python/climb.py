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
def climb(n, steps):
    count = 0
    if n<=1:
        count=1
    else:
        for step in steps:
            count += climb(n-step, steps)
    return count


def climb2(n, steps, cache=None):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    count = 0
    if n <= 1:
        return 1
    else:
        for step in steps:
            count += climb2(n-step, steps, cache)
            cache[n] = count
        return cache[n]

print climb(10, (1, 2))
print climb2(10, (1, 2))



