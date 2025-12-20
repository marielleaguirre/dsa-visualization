'''
Binary Tree Pseudocode

Key Classes:
- BinaryTree > generates an empty binary tree and will store the nodes produced by Nodes
- Nodes > handles the creation of left/right nodes
- Traversals > creates the traversal equivalents of the binary tree


'''

values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

class Node:

    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


class BinaryTree:
    
    def __init__(self):
        self.root = Node(None)

    def generate_tree(self, level):
        tree = []

        for _ in range(level-1):
            value = Node(input("Enter node value: "))
            value.left = Node(input("Enter left child value: "))
            value.right = Node(input("Enter right child value: "))
            tree.append(value)

        return tree


class Traversal:
    pass


bin_tree = BinaryTree()
tree = bin_tree.generate_tree(4)
length = len(tree)

for i in range(length):
    print(f"Node {i}: {tree[i].value}, Left Child: {tree[i].left.value}, Right Child: {tree[i].right.value}")

# # Simulation

# bin_tree = BinaryTree(1)
# bin_tree.root.left = Node(2)
# bin_tree.root.right = Node(3)

# #     1
# #    / \
# #   2   3

# bin_tree.root.left.left = Node(5)
# bin_tree.root.left.right = Node(4)
# bin_tree.root.right.left = Node(6)
# bin_tree.root.right.right = Node(7)

# #       1
# #      / \
# #     2   3
# #    / \ / \
# #   5  4 6  7