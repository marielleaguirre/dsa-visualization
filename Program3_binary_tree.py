'''
Binary Tree Pseudocode

Key Classes:
- BinaryTree > generates an empty binary tree and will store the nodes produced by Nodes
- Nodes > initiates the objects acting as nodes
- Traversals > creates the traversal equivalents of the binary tree


'''
class Node:
    
    def __init__(self, value=None):
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.value = value


class BinaryTree:
    def __init__(self, level):
        self.root = None
        self.level = level
        self.all_nodes = []

    def gen_node(self):
        return Node()
    
    def build_tree(self):
        if self.level <= 1:
            print("Invalid number of levels. Please enter a positive integer greater than 1.")
            return False
        
        self.root = self.gen_node()
        self.root.parent = 1
        self.all_nodes.append(self.root)

        total_nodes = 2**self.level - 1

        queue = [self.root]
        node_counder = 1

        while len(self.all_nodes) < total_nodes:
            current_node = queue.pop(0)

            left_child = self.gen_node()
            right_child = self.gen_node()

            current_node.left_child = left_child
            current_node.right_child = right_child

            left_child.parent = current_node
            right_child.parent = current_node

            queue.append(left_child)
            queue.append(right_child)

            self.all_nodes.append(left_child)
            self.all_nodes.append(right_child)

            node_counder += 2

    
    def insert_nodes(self):

        for index, node in enumerate(self.all_nodes, 1):
            while True:
                node_val = input(f"Node {index}/{len(self.all_nodes)}: ").strip()

                if node_val == ".":
                    node.value = None
                elif node.parent == None:
                    node.value = None
                else:
                    node.value = node_val
                break
                 
class Traversal:

    def __init__(self, bin_tree):
        self.bin_tree = bin_tree
        self.root = bin_tree.root
        self.all_nodes = bin_tree.all_nodes 

    def inorder_traversal(self):
        
        node = self.root

        result = []

        def inorder_resursively(curr_node):
            if curr_node is None:
                return
            inorder_resursively(curr_node.left_child)
            result.append(curr_node.value)
            inorder_resursively(curr_node.right_child)

        inorder_resursively(node)
        return result



if __name__ == "__main__":
    bin_tree = BinaryTree(2)
    bin_tree.build_tree()
    nodes = bin_tree.insert_nodes()

    bin_tree = Traversal(bin_tree)
    inorder = bin_tree.inorder_traversal()
    print(inorder)