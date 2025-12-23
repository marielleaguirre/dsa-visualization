'''
Binary Search Tree Pseudocode:
/ 1. Display a menu to choose input method:
    a. Random input
    b. User input
/ 2. Ask the user to enter the number of nodes (between 10 and 30)
/ 3. If the user chooses Random input:
    a. Generate n random integers
/ 4. If the user chooses User input:
    a. Prompt the user to enter n integers
/ 5. Create an empty Binary Search Tree (BST)
/ 6. For each number in the list:
    a. Insert the number into the BST following rules:
        i. If BST is empty, create root node
        ii. If number <= current node value, go to left node
        iii. If number > current node value, go to right node
        iv. Repeat until correct position is found
/ 7. Display the list of numbers entered/generated
/ 8. Perform and display the following traversals:
    a. Inorder Traversal (Left → Top → Right)
    b. Preorder Traversal (Top → Left → Right)
    c. Postorder Traversal (Left → Right → Top)
'''

import random

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value <= root.data:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

def display_bst(node, prefix="", is_left=True):
    if node.right is not None:
        display_bst(node.right, prefix + ("│   " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(node.data))
    if node.left is not None:
        display_bst(node.left, prefix + ("    " if is_left else "│   "), True)

def inorder_traversal(root):
    return inorder_traversal(root.left) + [root.data] + inorder_traversal(root.right) if root else []

def preorder_traversal(root):
    return [root.data] + preorder_traversal(root.left) + preorder_traversal(root.right) if root else []

def postorder_traversal(root):
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.data] if root else []

def main():
    print("Binary Search Tree Program")
    print("1 - Random Input")
    print("2 - User Input")

    choice = input("Choose input method (1 or 2): ")

    while True:
        node_count = int(input("Enter number of nodes (10-30): "))
        if 10 <= node_count <= 30:
            break
        print("Invalid. Please enter a valid number between 10 and 30.")

    numbers = []

    # Handle Random Input
    if choice == '1':
        numbers = [random.randint(1, 100) for _ in range(node_count)]

    # Handle User Input
    elif choice == '2':
        print("Enter integer values:")
        while len(numbers) < node_count:
            value = int(input(f"Value {len(numbers)+1}: "))
            numbers.append(value)
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