#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/29'
exchanges = False

# 平均时间复杂度：O(n2)
def bubbleSort(alist):
    for j in range(len(alist)-1,0,-1):
        for i in range(j):
            if alist[i] > alist[i+1]:
                alist[i], alist[i+1] = alist[i+1], alist[i]
        print alist

alist = [54,26,93,17,77,31,44,55,20]
bubbleSort(alist)
print(alist)