from others.misc_func import validate_input, clear_console

# Creates objects that defines a node, including its links to other nodes
class Node:
    
    def __init__(self, value=None):
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.value = value

# Class that stores the main algorithms of binary tree
class BinaryTree: 
    def __init__(self, level):
        self.root = None
        self.level = level 
        self.all_nodes = [] # Stores all the nodes inputted

    def gen_node(self): # A function that simplifies tha Node Class
        return Node()
    
    def build_tree(self): # Creates node placeholder based on the input level        
        # Manually initializes the characteristics for the root node
        self.root = self.gen_node()
        self.root.parent = 1 # Default 1, no reason for the value used
        self.all_nodes.append(self.root) # Records the first node/top node

        # Formula for calculating the total nodes based on levels
        total_nodes = 2**self.level - 1


        # Queue System/Breadth First Search(BFS) | MAIN ALGORITHM
        queue = [self.root] # initializes the root as the first in the queue
        node_counter = 1

        while len(self.all_nodes) < total_nodes:
            current_node = queue.pop(0) # Takes the first node in the queue

            # Initializes the left and child node
            left_child = self.gen_node()
            right_child = self.gen_node()

            # Assigns the children to the current node at hand
            current_node.left_child = left_child
            current_node.right_child = right_child

            # Sets the parent of each node 
            current_node.left_child.parent = current_node
            current_node.right_child.parent = current_node

            # Records the new nodes to the overall list
            self.all_nodes.append(current_node.left_child)
            self.all_nodes.append(current_node.right_child)

            # Adds the recorded nodes to the queue for later use (they will be popped FIFO manner just to assign children/parent values)
            queue.append(current_node.left_child)
            queue.append(current_node.right_child)

            # Handles the loop
            node_counter += 2

    
    # This is where the user can input/assign values to each placeholder in the initialized BinaryTree object
    def insert_nodes(self):

        # Prompt for user input
        for index, node in enumerate(self.all_nodes, 1):
            while True:
                prompt = f"Node {index}/{len(self.all_nodes)}: "
                node_val = validate_input(prompt)

                if node_val == ".":
                    node.value = None
                elif node.parent == None: # Will fix, may issues pa rin
                    node.value = None
                else:
                    node.value = node_val
                break

    # This only shows the metadata of each nodes, not the actual graph                 
    def show_tree_structure(self):
        for node in self.all_nodes:
            left_child = node.left_child.value if node.left_child else "None"
            right_child = node.right_child.value if node.right_child else "None"
            parent_node = node.parent if node.parent else "None"

            parent_node = parent_node.value if parent_node != 1 else "Parent Node"
            parent_node = parent_node.value if parent_node is not 1 else "Root"

            if parent_node is not None: 
                data_str = f"Node: {node.value}\n Parent Node: {parent_node}\n Left Child: {left_child}\n Right Child: {right_child}\n"
            else: # Excludes metadata of nodes w/o parent nodes
                data_str= f"Node: {node.value} does not exist. \n"

            print(data_str)


# Uses RECURSION as main algorithm
class Traversal:

    # Retrieve all necessary values
    def __init__(self, bin_tree):
        self.bin_tree = bin_tree
        self.root = bin_tree.root
        self.all_nodes = bin_tree.all_nodes 

    def inorder_traversal(self):
        
        node = self.root

        result = []

        # Recursion | created another function so that inorder_traversal won't need an argument
        def inorder_resursively(curr_node):
            if curr_node is None: # Searcher: if it does not find any value in the node, it stops the recursion
                return
            inorder_resursively(curr_node.left_child) # Find leftmost node, if it triggers the Searcher;
            result.append(curr_node.value) # retrieves the current node it is currently on
            inorder_resursively(curr_node.right_child) # Find rightmost node, if it does not find any leftmost node and triggers the Searcher, it retrieves current node

        inorder_resursively(node) 
        
        return result
    
    def preorder_traversal(self):
        
        node = self.root

        result = []

        def preorder_resursively(curr_node):
            if curr_node is None:
                return
            result.append(curr_node.value)
            preorder_resursively(curr_node.left_child)
            preorder_resursively(curr_node.right_child)

        preorder_resursively(node)

        return result
    
    def postorder_traversal(self):
        
        node = self.root

        result = []

        def postorder_resursively(curr_node):
            if curr_node is None:
                return
            postorder_resursively(curr_node.left_child)
            postorder_resursively(curr_node.right_child)
            result.append(curr_node.value)

        postorder_resursively(node)

        return result


def main():
    clear_console()
    border = 20 * "="
    print(border, "BINARY TREE GENERATOR", border)

    levels_query = "\nEnter the number of levels of your Binary Tree (1-5): "
    levels_input = int(validate_input(levels_query, [1, 2, 3, 4, 5]))

    bin_tree = BinaryTree(levels_input)
    bin_tree.build_tree()
    bin_tree.insert_nodes()
    print(bin_tree.all_nodes)
    bin_tree.show_tree_structure()

    print("\n", border, "TRAVERSALS (LTR, TLR, LRT)", border, "\n")

    bin_tree = Traversal(bin_tree)
    preorder = bin_tree.preorder_traversal()
    inorder = bin_tree.inorder_traversal()
    postorder = bin_tree.postorder_traversal()


    print(f"Preorder Traversal (TLR): {preorder}")
    print(f"Inorder Traversal (LTR): {inorder}")
    print(f"Postorder Traversal (LRT): {postorder}")
    print("")


if __name__ == "__main__":
    main()