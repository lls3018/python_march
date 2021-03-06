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
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fib2(n, cache):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n == 0 or n == 1:
        return 1
    else:
        cache[n] = fib2(n-1, cache) + fib2(n-2, cache)
        return cache[n]


def fib3(n):
    x, y = 0, 1
    while n:
        x, y = y, x+y
        n -= 1
    return y


def fib4(n):
    # write code here
    num=[]
    num.insert(0, 1)
    num.insert(1, 1)
    for i in range(2, n+1):
        num.insert(i, num[i-1] + num[i-2])
    return num[n]


print fib(10)
print fib2(10, cache = {})
print fib3(10)
print fib4(10)
