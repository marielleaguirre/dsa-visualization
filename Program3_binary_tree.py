'''
Binary Tree Pseudocode

Key Classes:
- BinaryTree > generates an empty binary tree and will store the nodes produced by Nodes
- Nodes > handles the creation of left/right nodes
- Traversals > creates the traversal equivalents of the binary tree


'''

values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

class Node:
    
    def __init__(self, value):
        self.left_child = None
        self.right_child = None
        self.value = value


class BinaryTree:
    def __init__(self):
        self.root = None

    def gen_node(self, value):
        return Node(value)
    
    def insert_node(self, curr_node, value):
        
        if curr_node is None:
            curr_node = self.gen_node(value)

        elif curr_node.left_child is None:
            curr_node.left_child = self.insert_node(curr_node.left_child, value)
        
        elif curr_node.right_child is None:
            curr_node.right_child = self.insert_node(curr_node.right_child, value)

        else:
            self.insert_node(curr_node.left_child, value)
            self.insert_node(curr_node.right_child, value)

        return curr_node
        

class Traversal:
    pass


bin_tree = BinaryTree()
for val in values:
    bin_tree.root = bin_tree.insert_node(bin_tree.root, val)
    print(f'Inserted {val} into the binary tree.')

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