#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/29'


def quickSort(alist):
    quickSortHelper(alist,0,len(alist)-1)


def quickSortHelper(alist, first, last):
    if first < last:
        splitpoint = partion(alist,first,last)
        quickSortHelper(alist, first, splitpoint-1)
        quickSortHelper(alist, splitpoint+1, last)


def partion(alist, first, last):
    pivotvalue = alist[first]
    left = first+1
    right = last

    done = False
    while not done:
        while left <= right and alist[left] < pivotvalue:
            left = left+1
        while alist[right] >= pivotvalue and right >=left:
            right = right-1
        if right < left:
            done = True
        else:
            alist[left], alist[right] = alist[right], alist[left]

    alist[first], alist[right] = alist[right], alist[first]
    return right

alist = [54,26,93,17,77,31,44,55,20]
quickSort(alist)
print(alist)