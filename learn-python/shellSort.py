#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/29'


def shellSort(alist):
    sublistcount = len(alist)//2
    while sublistcount > 0:
        for startposition in range(sublistcount):
            gapInsertionSort(alist, startposition, sublistcount)

        print("After increments of size", sublistcount,
              "The list is", alist)

        sublistcount = sublistcount//2


def gapInsertionSort(alist,start,gap):
    for i in range(start+gap, len(alist),gap):
        currentvalue = alist[i]
        positon = i

        while positon >= gap and alist[positon-gap] > currentvalue:
            alist[positon] = alist[positon-gap]
            positon = positon-gap

        alist[positon]=currentvalue

alist = [54,26,93,17,77,31,44,55,20]
shellSort(alist)
print(alist)