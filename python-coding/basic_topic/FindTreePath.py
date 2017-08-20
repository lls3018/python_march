# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    '''
    输入一颗二叉树和一个整数，打印出二叉树中结点值的和为输入整数的所有路径。
    路径定义为从树的根结点开始往下一直到叶结点所经过的结点形成一条路径。
    '''
    # 返回二维列表，内部每个列表表示找到的路径
    def FindPath(self, root, expectNumber):
        # write code here
        if not root:
            return []
        ret = []
        path = []
        self.Find(root, expectNumber, ret, path)
        return ret

    def Find(self, root, target, ret, path):
        if not root:
            return
        path.append(root.val)
        isLeaf = (root.left is None and root.right is None)
        if isLeaf and target == root.val:
            ret.append(path[:])
        if root.left:
            self.Find(root.left, target - root.val, ret, path)
        if root.right:
            self.Find(root.right, target - root.val, ret, path)
        path.pop()