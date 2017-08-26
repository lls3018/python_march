"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    # @param {TreeNode} root the root of binary tree
    # @param {int} target an integer
    # @return {int[][]} all valid paths
    def binaryTreePathSum(self, root, target):
        # Write your code here
        '''
        给定一个二叉树，找出所有路径中各节点相加总和等于给定 目标值 的路径。
        一个有效的路径，指的是从根节点到叶节点的路径。
        '''
        res = []
        self.helper(root, target, res, [])
        return res

    def helper(self, root, target, result, path):
        if root:
            remain = target - root.val
            if remain == 0 and root.left is None and root.right is None:
                result.append(path + [root.val])
            else:
                path.append(root.val)
                self.helper(root.left, remain, result, path)
                self.helper(root.right, remain, result, path)
                path.pop()