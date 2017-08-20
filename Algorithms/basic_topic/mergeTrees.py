#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/7/11'


class TreeNode(object):
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None

def mergeTrees(t1, t2):
    if t1 is None:
        return t2
    if t2 is None:
        return t1
    t = TreeNode(t1.val + t2.val)
    t.left = mergeTrees(t1.left, t2.left)
    t.right = mergeTrees(t1.right, t2.right)
    return t
