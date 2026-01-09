import pygame
import sys
import time

# -------------------- CONFIG --------------------
WIDTH, HEIGHT = 1000, 560  # Window size
FPS = 60  # Frames per second for smooth rendering

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")
clock = pygame.time.Clock()