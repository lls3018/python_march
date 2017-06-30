#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/6/29'


def selectionSort(alist):
    for fillslot in range(len(alist)-1,0,-1):
        pos_max = 0
        for i in range(1,fillslot+1):
            if alist[i] > alist[pos_max]:
                pos_max = i
        alist[pos_max], alist[fillslot] = alist[fillslot], alist[pos_max]

alist = [54,26,93,17,77,31,44,55,20]
selectionSort(alist)
print(alist)