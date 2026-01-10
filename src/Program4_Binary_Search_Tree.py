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
