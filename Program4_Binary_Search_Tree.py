import random

class Node:
    def __init__(self, data):  # Initialize a BST node with data and left/right children
        self.data = data
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:  # If the tree is empty, create a new node
        return Node(value)
    if value <= root.data:  
        root.left = insert(root.left, value)  # If value is smaller or equal, go to left subtree
    else:
        root.right = insert(root.right, value)  # If value is larger, go to right subtree
    return root

def display_bst(node, prefix="", is_left=True):  # Display BST in a sideways tree structure
    if node.right is not None:
        display_bst(node.right, prefix + ("│   " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(node.data))
    if node.left is not None:
        display_bst(node.left, prefix + ("    " if is_left else "│   "), True)

def inorder_traversal(root):  # Traverse BST: Left → Root → Right
    return inorder_traversal(root.left) + [root.data] + inorder_traversal(root.right) if root else []

def preorder_traversal(root):  # Traverse BST: Root → Left → Right
    return [root.data] + preorder_traversal(root.left) + preorder_traversal(root.right) if root else []

def postorder_traversal(root):  # Traverse BST: Left → Right → Root
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.data] if root else []

def main():
    print("Binary Search Tree Program")
    print("1 - Random Input")
    print("2 - User Input")

    while True:  # Validate menu choice
        choice = input("\nChoose input method (1 or 2): ")
        if choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")

    while True:  # Validate number of nodes
        try: 
            node_count = int(input("\nEnter number of nodes (10-30): "))
            if 10 <= node_count <= 30:
                break
            else:      
                print("Invalid. Please enter a valid number between 10 and 30.")  
        except ValueError:
            print("Invalid. Please enter an integer.")

    numbers = []

    # Handle Random Input
    if choice == '1':
        numbers = [random.randint(1, 100) for _ in range(node_count)]

    # Handle User Input
    elif choice == '2':
        print("\nEnter integer values:")
        while len(numbers) < node_count:
            try:
                value = int(input(f"Value {len(numbers)+1}: "))
                numbers.append(value)
            except ValueError:
                print("Invalid. Please enter an integer.")
    else:
        print("Invalid choice.")
        return
    
    root = None
    for node_value in numbers:
        root = insert(root, node_value)

    print("\nNumber List:")
    print(numbers)

    print("\nEquivalent Binary Search Tree:")
    display_bst(root)

    print("\nInorder Traversal (Left → Top → Right):")
    print(inorder_traversal(root))

    print("\nPreorder Traversal (Top → Left → Right):")
    print(preorder_traversal(root))

    print("\nPostorder Traversal (Left → Right → Top):")
    print(postorder_traversal(root))

main()