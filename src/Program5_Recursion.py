import pygame
import sys
import time

# -------------------- CONFIG --------------------
WIDTH, HEIGHT = 1000, 560  # Window size
FPS = 60  # Frames per second for smooth rendering

ROD_Y = 400           # Base y-position for rods
ROD_HEIGHT = 260      # Height of rods
DISK_HEIGHT = 26      # Height of each disk
DISK_WIDTH_STEP = 36  # Width increase per disk size
MOVE_DELAY = 0.5      # Delay between disk moves

# Colors
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)
WOOD = (139, 94, 60)  # Rods and base
TEXT_LIGHT = (240, 240, 240)
DISK_COLORS = [       # Different colors for each disks
    (255, 99, 132),
    (255, 159, 64),
    (255, 205, 86),
    (75, 192, 192),
    (54, 162, 235),
    (153, 102, 255),
    (201, 203, 207)
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")
clock = pygame.time.Clock()

# Fonts for UI text
font = pygame.font.SysFont("Georgia", 24)
big_font = pygame.font.SysFont("Georgia", 40, bold=True)
title_font = pygame.font.SysFont("Georgia", 46, bold=True)

# -------------------- DISK --------------------
class Disk:
    """ Represents a single disk in the Tower of Hanoi """
    def __init__(self, size):
        self.size = size
        self.color = DISK_COLORS[size - 1]  # Assign color based on size

# -------------------- ROD --------------------
class Rod:
    """ Represents a rod with a stack of disks """
    def __init__(self, name, x):
        self.name = name
        self.x = x         # X-position on the screen
        self.stack = []    # Stack of disks ont his rod

    def push(self, disk):
        """" Add a disk to the top of the rod """
        self.stack.append(disk)

    def pop(self):
        """ Remove and return the top disk from the rod """
        return self.stack.pop() if self.stack else None

# -------------------- HANOI GAME --------------------
class HanoiGame:
    """ Handles Tower of Hanoi logic and rendering """
    def __init__(self, num_disks):
        self.num_disks = num_disks
        # Create three rods (A, B, C) with positions
        self.rods = {
            'A': Rod('A', WIDTH // 2 - 260),
            'B': Rod('B', WIDTH // 2),
            'C': Rod('C', WIDTH // 2 + 260)
        }
        self.moves = []      # List of moves to solve the puzzle
        self.move_count = 0  # Count of moves made
        self.reset()         # Initialize game