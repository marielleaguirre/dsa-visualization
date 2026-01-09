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

    # Tower of Hanoi algorithm
    def tower_of_hanoi(self, n, source, auxiliary, target):
        """ Recursive Tower of Hanoi solution """
        if n == 1:
            self.moves.append((source, target))  # Record the move
            return
        self.tower_of_hanoi(n - 1, source, target, auxiliary)
        self.moves.append((source, target))
        self.tower_of_hanoi(n - 1, auxiliary, source, target)

    # Reset the game
    def reset(self):
        """ Reset the game to initial state """
        self.rods['A'].stack = [Disk(i) for i in range(self.num_disks, 0, -1)]  # Fill A rod
        self.rods['B'].stack = []
        self.rods['C'].stack = []
        self.moves = []
        self.move_count = 0
        self.tower_of_hanoi(self.num_disks, 'A', 'B', 'C')  # Precompute solution moves

    def move_disk(self, source, target):
        """ Move a disk from one rod to another visually """
        disk = self.rods[source].pop()  # Remove disk from source rod
        self.rods[target].push(disk)    # Add disk to target rod
        self.move_count += 1            # Increment move counter
        self.redraw(highlight=disk)     # Redraw with animation
        time.sleep(MOVE_DELAY)          # Small delay for visualization

    # ---------------- Drawing ----------------
    def draw_gradient(self):
        """ Draw a dark blue gradient background """
        for y in range(HEIGHT):
            color = (30 + y // 12, 30 + y // 12, 70 + y // 6)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    def draw_rods(self):
        """ Draw rods and base """
        base_y = ROD_Y + 18
        base_width = 260 * 2 + 200
        # Base
        pygame.draw.rect(screen, WOOD, (WIDTH // 2 - base_width // 2, base_y, base_width, 14), border_radius=8)
        # Rods
        for rod in self.rods.values():
            pygame.draw.rect(screen, WOOD, (rod.x - 8, base_y - ROD_HEIGHT, 16, ROD_HEIGHT), border_radius=6)

    def draw_disks(self, highlight=None):
        """ Draw all disks on rods """
        for rod in self.rods.values():
            for i, disk in enumerate(rod.stack):
                width = disk.size * DISK_WIDTH_STEP
                x = rod.x - width // 2
                y = ROD_Y - i * DISK_HEIGHT
                pygame.draw.rect(screen, disk.color, (x, y, width, DISK_HEIGHT), border_radius=9)
                if highlight == disk:  # Highlight recently moved disk
                    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, width + 6, DISK_HEIGHT + 6), 2, border_radius=11)
    
    def draw_ui(self, solved=False):
        """ Draw UI elements like title, move count, optimal moves """
        title = title_font.render("Tower of Hanoi", True, TEXT_LIGHT)
        screen.blit(title, (WIDTH // 2 - 180, 20))
        moves_text = font.render(f"Moves: {self.move_count}", True, TEXT_LIGHT)
        optimal_text = font.render(f"Optimal: {2 ** self.num_disks - 1}", True, TEXT_LIGHT)
        screen.blit(moves_text, (40, 90))
        screen.blit(optimal_text, (40, 120))
        info = font.render("R = Restart   ESC = Exit", True, TEXT_LIGHT)
        screen.blit(info, (WIDTH - 300, 100))
        if solved:
            win = big_font.render("Puzzle Solved!", True, (255, 215, 0))
            screen.blit(win, (WIDTH // 2 - 190, HEIGHT // 2 - 40))

    def redraw(self, highlight=None, solved=False):
        """ Full redraw of game """
        self.draw_gradient()
        self.draw_rods()
        self.draw_disks(highlight)
        self.draw_ui(solved)
        pygame.display.flip()


# -------------------- MENU CLASS --------------------
class Menu:
    """ Handles disk number selection """
    def __init__(self):
        self.selected = ""  # User-selected number
        self.message = ""   # Error or info messages