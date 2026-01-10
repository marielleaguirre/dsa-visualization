import pygame
import sys
import random

pygame.init()  # Initialize all Pygame modules

# -------------------- FULLSCREEN SETUP --------------------
info = pygame.display.Info()  # Get info about the current display
WIDTH, HEIGHT = info.current_w, info.current_h  # Fullscreen width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Fullscreen window
pygame.display.set_caption("Binary Search Tree Visualizer")  # Set window title

# -------------------- FONTS --------------------
# Fonts for different UI elements
FONT = pygame.font.SysFont("consolas", 22)       # Regular text
BIG_FONT = pygame.font.SysFont("consolas", 36)   # Big title text
NODE_FONT = pygame.font.SysFont("consolas", 24, bold=True)  # Node numbers in the tree

# -------------------- COLORS --------------------
# Background gradient
BG_TOP = (200, 230, 255)    # Top of gradient (light blue)
BG_BOTTOM = (245, 250, 255) # Bottom of gradient (almost white)
PANEL = (245, 245, 245)     # Sidebar panel background

# Standard colors
BLACK = (40, 40, 40)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (60, 180, 120)
RED = (220, 90, 90)

# Button colors
BTN = (88, 101, 242)        # Normal button color
BTN_HOVER = (114, 137, 218) # Hover color

# Node colors (random for visual variety)
NODE_COLORS = [(100, 149, 237), (255, 140, 0), (60, 180, 120), (255, 105, 180), (138, 43, 226)]

# Warning text color
WARN = (220, 50, 50)

clock = pygame.time.Clock()  # Clock to control FPS
MAX_NODES = 30               # Maximum allowed nodes in BST


# -------------------- BST NODE CLASS --------------------
class Node:
    """Represents a single node in the BST."""
    def __init__(self, data, x=0, y=0):  
        self.data = data     # Value stored in the node
        self.left = None     # Left child
        self.right = None    # Right child
        self.x = x            # X-coordinate for drawing
        self.y = y            # Y-coordinate for drawing
        self.color = random.choice(NODE_COLORS)  # Random color for node
        self.radius = 26      # Node radius for drawing
        self.growth = 0       # Used for "pop-in" animation effect

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