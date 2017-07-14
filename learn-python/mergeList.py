#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/7/8'

'''
按升序合并如下两个list, 并去除重复的元素
先选一个中间数，然后一边是小的数字，一边是大的数字，
然后再循环递归，排完序(是不是想起了c里面的冒泡)
'''

import random


def qsort(L):
    if len(L) < 2:
        return L
    pivot_element = random.choice(L)
    small = [i for i in L if i < pivot_element]
    large = [i for i in L if i > pivot_element]
    return qsort(small) + [pivot_element] + qsort(large)


def merge(list1, list2):
    return qsort(list1+list2)

list1 = [2,3,8,4,9,5,6]
list2 = [5,6,10,17,11,2]
print merge(list1, list2)