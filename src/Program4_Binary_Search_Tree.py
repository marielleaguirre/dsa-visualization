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

# -------------------- BUTTON CLASS --------------------
class Button:
    """Represents a clickable button in the UI."""
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)  # Button rectangle (position + size)
        self.text = text                      # Button text
    
    def draw(self):
        """Draw the button, change color on hover."""
        hover = self.rect.collidepoint(pygame.mouse.get_pos())  # Check if mouse is over button
        color = BTN_HOVER if hover else BTN                     # Change color if hovering
        pygame.draw.rect(screen, color, self.rect, border_radius=12)  # Fill rectangle
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=12)  # Draw border
        txt = FONT.render(self.text, True, WHITE)               # Render button text
        screen.blit(txt, txt.get_rect(center=self.rect.center))  # Center text inside button

    def clicked(self, event):
        """Check if button is clicked based on mouse event."""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# -------------------- INPUT BOX CLASS --------------------
class InputBox:
    """Represents a text input box for user to enter numbers."""
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)  # Rectangle for input box
        self.text = ""                        # Current text
        self.active = False                    # Whether box is active (clicked)

    def draw(self):
        """Draw the input box with border highlight if active."""
        color_border = BTN if self.active else BLACK  # Highlight if active
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=6)   # Fill box white
        pygame.draw.rect(screen, color_border, self.rect, 3, border_radius=6)  # Border
        txt = FONT.render(self.text, True, BLACK)     # Render text
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))  # Draw inside box

    def handle(self, event):
        """Handle mouse click activation and keyboard input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activate box if clicked
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Delete last character
            elif event.unicode.isdigit():
                self.text += event.unicode  # Add digit to text

# -------------------- BST VISUALIZER CLASS --------------------
class BSTVisualizer:
    """Main class for handling BST logic, drawing, and traversals."""
    def __init__(self):
        self.root = None           # Root node of BST
        self.numbers = []          # Numbers to insert into BST
        self.insert_index = 0      # Index of next number to insert
        self.warning_text = ""     # Any warning messages

        # ---------- INSERT NODE ----------
    def insert(self, root, value):
        """Recursively insert a value into the BST."""
        if root is None:
            return Node(value)  # Create new node if current is empty
        if value <= root.data:
            root.left = self.insert(root.left, value)   # Go left
        else:
            root.right = self.insert(root.right, value) # Go right
        return root
    
    # ---------- ASSIGN NODE POSITIONS ----------
    def assign_positions(self, node=None, depth=0, x_min=220, x_max=None, y_start=140, y_gap=100):
        """Assign x, y coordinates to each node for visualization."""
        if node is None:
            node = self.root
        self._assign_positions_recursive(node, depth, x_min, x_max, y_start, y_gap)

    def _assign_positions_recursive(self, node, depth, x_min, x_max, y_start, y_gap):
        if not node:
            return
        if x_max is None:
            x_max = WIDTH - 20
        node.y = y_start + depth * y_gap              # Vertical spacing per depth
        node.x = (x_min + x_max) // 2                 # Horizontal center of subtree
        # Assign positions recursively to left and right children
        self._assign_positions_recursive(node.left, depth + 1, x_min, node.x - 10, y_start, y_gap)
        self._assign_positions_recursive(node.right, depth + 1, node.x + 10, x_max, y_start, y_gap)

    # ---------- DRAW TREE ----------
    def draw_tree(self, node):
        """Recursively draw nodes and edges of the BST."""
        if not node:
            return
        # Draw lines to children first (edges)
        if node.left:
            pygame.draw.line(screen, BLACK, (node.x, node.y), (node.left.x, node.left.y), 2)
            self.draw_tree(node.left)
        if node.right:
            pygame.draw.line(screen, BLACK, (node.x, node.y), (node.right.x, node.right.y), 2)
            self.draw_tree(node.right)
        # Pop-in animation for node
        if node.growth < node.radius:
            node.growth += 2
        pygame.draw.circle(screen, node.color, (node.x, node.y), node.growth)      # Node fill
        pygame.draw.circle(screen, BLACK, (node.x, node.y), node.growth, 2)       # Node border
        txt = NODE_FONT.render(str(node.data), True, WHITE)                        # Node number
        screen.blit(txt, txt.get_rect(center=(node.x, node.y)))                    # Draw number
    
    # ---------- TREE TRAVERSALS ----------
    def inorder(self, root):
        """Return inorder traversal as a list."""
        return self.inorder(root.left) + [root.data] + self.inorder(root.right) if root else []

    def preorder(self, root):
        """Return preorder traversal as a list."""
        return [root.data] + self.preorder(root.left) + self.preorder(root.right) if root else []

    def postorder(self, root):
        """Return postorder traversal as a list."""
        return self.postorder(root.left) + self.postorder(root.right) + [root.data] if root else []

# -------------------- MAIN LOOP --------------------
def main():
    bst = BSTVisualizer()  # Initialize BST

    # -------------------- UI ELEMENTS --------------------
    input_box = InputBox(20, 120, 180, 40)       # Input box for user numbers
    random_btn = Button(20, 180, 180, 40, "Random Input")  # Fill BST with random numbers
    add_btn = Button(20, 230, 180, 40, "Add Number")       # Add single number
    insert_btn = Button(20, 280, 180, 40, "Insert Next")   # Insert next number from list
    restart_btn = Button(20, 330, 180, 40, "Restart")      # Clear everything
    exit_btn = Button(20, 380, 180, 40, "Exit")            # Exit program

    running = True
    while running:
        # -------------------- DRAW GRADIENT BACKGROUND --------------------
        for y in range(HEIGHT):
            color = (
                BG_TOP[0] + (BG_BOTTOM[0]-BG_TOP[0])*y//HEIGHT,
                BG_TOP[1] + (BG_BOTTOM[1]-BG_TOP[1])*y//HEIGHT,
                BG_TOP[2] + (BG_BOTTOM[2]-BG_TOP[2])*y//HEIGHT,
            )
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))  # Gradient background

        # -------------------- SIDEBAR PANEL --------------------
        pygame.draw.rect(screen, PANEL, (0, 0, 220, HEIGHT))  # Sidebar background
        pygame.draw.line(screen, BLACK, (220, 0), (220, HEIGHT), 3)  # Panel border

        # -------------------- TITLE --------------------
        title_surface = BIG_FONT.render("BINARY SEARCH TREE", True, BLACK)
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2 + 2, 22))  # Shadow
        screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 20))      # Main title

        # -------------------- EVENT HANDLING --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:        # Close button
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # ESC key
                running = False

            input_box.handle(event)  # Handle input box clicks and typing

            # -------------------- BUTTON CLICKS --------------------
            if random_btn.clicked(event):
                n = random.randint(10, 30)  # Random number of nodes
                bst.numbers = [random.randint(1, 99) for _ in range(n)]  # Random values
                if len(bst.numbers) > MAX_NODES:
                    bst.numbers = bst.numbers[:MAX_NODES]  # Limit nodes
                bst.root = None
                bst.insert_index = 0
                bst.warning_text = ""