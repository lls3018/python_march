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


def partion(alist, left, right):
    pivotvalue = alist[left]
    while left < right:
        while left < right and alist[right] >= pivotvalue:
            right = right-1
        alist[left] = alist[right]
        while left < right and alist[left] < pivotvalue:
            left = left+1
        alist[right] = alist[left]

    alist[left] = pivotvalue
    return left


#----
def qsort(alist):
    if alist == []:
        return []
    else:
        pivot = alist[0]
        left = qsort([x for x in alist[1:] if x < pivot])
        right = qsort([x for x in alist[1:] if x > pivot])
        return left + [pivot] + right




alist = [54,26,93,17,77,31,44,55,20]
quickSort(alist)
print(alist)

alist = [54,26,93,17,77,31,44,55,20]
print qsort(alist)
