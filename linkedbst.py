"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import time
import random

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        stack = LinkedStack()
        current = self._root
        done = False

        while not done:
            if current is not None:
                stack.push(current)
                current = current.left
            elif not stack.isEmpty():
                current = stack.pop()
                yield current.data
                current = current.right
            else:
                done = True


    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while node is not None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        newNode = BSTNode(item)
        if self.isEmpty():
            self._root = newNode
        else:
            node = self._root
            parent = None
            while node:
                parent = node
                if item < node.data:
                    node = node.left
                else:
                    node = node.right
            if item < parent.data:
                parent.left = newNode
            else:
                parent.right = newNode
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                left_height = height1(top.left)
                right_height = height1(top.right)
                return max(left_height, right_height) + 1
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        n = len([_ for _ in self.inorder()])
        if self.height() <= 2 * log(n + 1, 2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        data = [_ for _ in self.inorder()]
        return [v for v in data if low <= v <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_tree(lst, start, end):
            '''
            Build rebalanced tree.
            :return:
            '''
            if start > end:
                return None
            middle = (start + end) // 2
            node = BSTNode(lst[middle])
            node.left = build_tree(lst, start, middle - 1)
            node.right = build_tree(lst, middle + 1, end)
            return node

        inorder_list = [_ for _ in self.inorder()]
        self.clear()
        self._root = build_tree(inorder_list, 0, len(inorder_list) - 1)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        successor = None
        root = self._root
        while root:
            if root.data > item:
                if not successor or successor > root.data:
                    successor = root.data
                root = root.left
            else:
                root = root.right
        return successor

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        predecessor = None
        root = self._root
        while root:
            if root.data < item:
                if not predecessor or predecessor < root.data:
                    predecessor = root.data
                root = root.right
            else:
                root = root.left
        return predecessor
        
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        #Using list
        words = self.read_file(path)
        start1 = time.time()
        words = sorted(words)[0:1000]
        print(f"Time to find first 1000 sorted words from the file using list: {time.time() - start1}")

        #Using tree and sorted sourcecollection
        words = self.read_file(path)
        words = sorted(words)
        start2 = time.time()
        tree1 = LinkedBST(words)
        words = sorted(list(tree1.inorder())[0:1000])
        print(f"Time to find first 1000 sorted words from the file using tree in alphabetic order: {time.time() - start2}")

        #Using tree and shuffled sourcecollection
        words = self.read_file(path)
        random.shuffle(words)
        start3 = time.time()
        tree2 = LinkedBST(words)
        words = sorted(list(tree2.inorder())[0:1000])
        print(f"Time to find first 1000 sorted words from the file using tree randomly added: {time.time() - start3}")
    
        #Using balanced tree
        words = self.read_file(path)
        start4 = time.time()
        tree3 = LinkedBST(words)
        tree3.rebalance()
        words = sorted(list(tree3.inorder())[0:1000])
        print(f"Time to find first 1000 sorted words from the file using balanced tree: {time.time() - start4}")

    def read_file(self, path):
        """
        Reads tree from file.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().splitlines()

bst = LinkedBST()
bst.demo_bst('words.txt')