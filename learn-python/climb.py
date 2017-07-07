#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/30'

'''
题目描述
一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法。
'''


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
    if n <= 1:
        count = 1
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


def climb3(number):
    # write code here
    ans = []
    ans.append(0)
    ans.append(1)
    ans.append(2)
    for i in range(3, number + 1):
        ans.append(ans[i - 1] + ans[i - 2])
    return ans[number]


print climb(10, (1, 2))
print climb2(10, (1, 2))
print climb3(10)



