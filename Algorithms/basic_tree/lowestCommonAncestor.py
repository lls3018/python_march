"""
Definition of TreeNode:
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
"""


class Solution:
    """
    @param root: The root of the binary search tree.
    @param A and B: two nodes in a Binary.
    @return: Return the least common ancestor(LCA) of the two nodes.
    """

    def lowestCommonAncestor(self, root, A, B):
        # write your code here
        '''
        给定一棵二叉树，找到两个节点的最近公共父节点(LCA)。
        最近公共祖先是两个节点的公共的祖先节点且具有最大深度。
        '''
        if not root or A == root or B == root:
            return root

        left_lca = self.lowestCommonAncestor(root.left, A, B)
        right_lca = self.lowestCommonAncestor(root.right, A, B)

        if left_lca and right_lca:
            return root
        if left_lca:
            return left_lca
        if right_lca:
            return right_lca
        else:
            return None
