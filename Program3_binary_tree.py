'''
Binary Tree Pseudocode

Key Classes:
- BinaryTree > generates an empty binary tree and will store the nodes produced by Nodes
- Nodes > handles the creation of left/right nodes
- Traversals > creates the traversal equivalents of the binary tree


'''

values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

class Node:
    
    def __init__(self, value=None):
        self.left_child = None
        self.right_child = None
        self.value = value


class BinaryTree:
    
    def __init__(self, level=2):
        self.root = None
        self.nodes_n = 2**level - 1
        self.nodes_counter = 1


    def insert_node(self, value):
        if self.root is None:
            self.root = Node(value)
            return self.root
        else:
            node_val = self._insert_recursively(value, self.root)
            self.nodes_counter += 1
            return node_val

    
    def _insert_recursively(self, value, current_node):
        if current_node.left_child is None:
            print("Parent Node", current_node.value)
            current_node.left_child = Node(value)
            return current_node.left_child
        elif current_node.right_child is None:
            current_node.right_child = Node(value)
            print(f"====== {current_node.value}")
            return current_node.right_child
        elif self.check_full() is True:
            left_insert = self._insert_recursively(value, current_node.left_child)
            if left_insert is not None:
                return left_insert
            right_insert = self._insert_recursively(value, current_node.right_child)
            return right_insert
        else:
            return None
        
    def check_full(self):
        return self.nodes_counter == self.nodes_n

class Traversal:
    pass


bin_tree = BinaryTree()
for val in values:
    node = bin_tree.insert_node(val)
    print(node.value, "----")
    print("Nodes Counter:", bin_tree.nodes_counter)
    print("Is Full?:", bin_tree.check_full())

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