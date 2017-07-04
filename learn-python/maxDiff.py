#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/7/4'


'''
一个数组a[0...n-1]，求a[j]-a[i]的最大值，其中i<j
其中数组a[n]是无序

第一种方法：

从左往右求下标0到 k - 1 的最小值MIN
从右往左求 下标k到n -1 的最大值MAX
对于每个k都有一个MAX - MIN的值，最后求这个值的最大值即可。
例如数组：4 5 2 6 3 1
K：1 2 3 4 5
MIN： 4 4 2 2 2
MAX：6 6 6 3 1
MAX - MIN，最大的值为6 - 2 = 4， 即为结果

第二种方法：
令b[j] = a[j + 1] - a[j]，
那么a[j] - a[i]=(a[i+1]-a[i])+(a[i+2]-a[i+1])+...+(a[j]-a[i-1])
                   = b[i] +b[i+1]+ ...+ b[j - 1]，
即将问题转化成求一个数组子序列的最大值。这个过程的算法是有O(n)的算法的。
'''



def getMaxDiff(num_list):
    diff = 0
    i,j = 0,1
    for k in range(len(num_list)-1):
        if num_list[i] > num_list[j]:
            i=j
            if j == len(num_list):
                break
            j = j + 1
        tmp = num_list[j] - num_list[i]
        if tmp > diff:
            diff = tmp
        j = j+ 1
        if j == len(num_list):
            break
    return diff

list1 = [7,3,4,2,10,8,9,18,14,20]

list2 = [-2,2,-3,4,-1,2,1,-5,3]

print getMaxDiff(list1)
print getMaxDiff(list2)

