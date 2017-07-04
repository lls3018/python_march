#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/29'


def insertSort(alist):
    for i in range(1, len(alist)):
        currentvalue = alist[i]
        positon = i
        while positon > 0 and alist[positon-1] > currentvalue:
            alist[positon] = alist[positon-1]
            positon = positon-1

        alist[positon] = currentvalue
        print alist

alist = [54,26,93,17,77,31,44,55,20]
print alist
insertSort(alist)
print(alist)