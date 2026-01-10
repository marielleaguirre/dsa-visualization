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
