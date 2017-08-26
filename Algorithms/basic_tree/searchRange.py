"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""

class Solution:
    """
    @param: root: param root: The root of the binary search tree
    @param: k1: An integer
    @param: k2: An integer
    @return: return: Return all keys that k1<=key<=k2 in ascending order
    """

    def __init__(self):
        self.return_list = []

    def searchRange(self, root, k1, k2):
        '''
        给定两个值 k1 和 k2（k1 < k2）和一个二叉查找树的根节点。
        找到树中所有值在 k1 到 k2 范围内的节点。即打印所有x (k1 <= x <= k2) 
        其中 x 是二叉查找树的中的节点值。返回所有升序的节点值。
        
        树的中序遍历，遍历过程是需要比较k1,k2，只有在区间里的才遍历得到
        '''
        # write your code here
        if root is None:
            return self.return_list

        if root.left:
            self.searchRange(root.left, k1, k2)

        if k1 <= root.val <= k2:
            self.return_list.append(root.val)

        if root.right:
            self.searchRange(root.right, k1, k2)

        return self.return_list