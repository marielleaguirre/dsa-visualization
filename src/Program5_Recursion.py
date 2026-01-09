import pygame
import sys
import time

# -------------------- CONFIG --------------------
WIDTH, HEIGHT = 1000, 560  # Window size
FPS = 60  # Frames per second for smooth rendering

# Colors
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)
WOOD = (139, 94, 60)  # Rods and base
TEXT_LIGHT = (240, 240, 240)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")
clock = pygame.time.Clock()

# Fonts for UI text
font = pygame.font.SysFont("Georgia", 24)
big_font = pygame.font.SysFont("Georgia", 40, bold=True)
title_font = pygame.font.SysFont("Georgia", 46, bold=True)