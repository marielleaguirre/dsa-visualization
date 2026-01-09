"""
Stacks Parking Garage PseudoCode:
 1. Create a storage and set max capacity
    *10 Max Capacity
 2. Give out option for the user to:
    *Park the Car
      - Insert the Car to the Stack
    *Depart the Car
      - Remove the Car from the Stack
    *View Car
      - View the Car, displaying its details
    *Exit
      -Exit the program
 3. Create a program that organizes the Car using Stacks
    *LIFO(Last in First Out)
"""
import pygame
from datetime import datetime


# This class acts as a blueprint for vehicles
class Vehicle:
    def __init__(self, plate):
        # Store the vehicle's license plate
        self.plate = plate

        # Record the arrival time when the object is created
        self.arrival = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Departure time is None while the vehicle is parked
        self.departure = None

    def depart(self):
        # Record the time when the vehicle leaves the garage
        self.departure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# This class manages parking using a STACK (LIFO)

class ParkingGarageStacks:
    def __init__(self):
        # Maximum number of vehicles allowed
        self.garage_capacity = 10

        # Stack implemented using a Python list
        self.stack = []

        # Counter for occupied slots
        self.occupied = 0

    def park(self, plate):
        # Check if the vehicle is already parked
        if plate in [v.plate for v in self.stack]:
            return f"Vehicle {plate} is already parked."

        # Check if the garage is full
        if self.occupied >= self.garage_capacity:
            return "Garage is FULL."

        # Create a new vehicle object
        vehicle = Vehicle(plate)

        # Push vehicle onto the stack
        self.stack.append(vehicle)
        self.occupied += 1

        # Return success message
        return f"Vehicle {plate} parked at {vehicle.arrival}"

    def depart(self, plate):
        # Temporary stack to hold blocking vehicles
        temp_stack = []
        found = False

        # Pop vehicles until target is found
        while self.stack:
            vehicle = self.stack.pop()

            # If this is the target vehicle
            if vehicle.plate == plate:
                vehicle.depart()
                self.occupied -= 1
                found = True
                message = f"Vehicle {plate} departed at {vehicle.departure}"
                break
            else:
                # Store blocking vehicles temporarily
                temp_stack.append(vehicle)

        # Restore the vehicles back to the main stack
        while temp_stack:
            self.stack.append(temp_stack.pop())

        # If vehicle was not found
        if not found:
            return f"Vehicle {plate} not found."

        return message



pygame.init()                                  # Initialize pygame modules

WIDTH, HEIGHT = 900, 600                       # Window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parking Garage Stack Simulation")

font = pygame.font.Font(None, 28)              # Font for text
clock = pygame.time.Clock()                    # Controls frame rate

# Create parking garage object
garage = ParkingGarageStacks()

# Variables for text input and messages
input_text = ""
active_input = False
mode = None                                   # "park" or "depart"
message = ""

# Define buttons (x, y, width, height)
park_btn = pygame.Rect(650, 100, 200, 40)
depart_btn = pygame.Rect(650, 160, 200, 40)

def draw_text(text, x, y, color=(255, 255, 255)):
    """
    Renders text on the pygame window
    """
    screen.blit(font.render(text, True, color), (x, y))

# Main function to run the parking garage program

running = True
while running:
    screen.fill((25, 25, 25))                  # Clear screen (dark gray)

    # =========================
    # EVENT HANDLING
    # =========================
    for event in pygame.event.get():

        # Exit program when window is closed
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If PARK button is clicked
            if park_btn.collidepoint(event.pos):
                active_input = True
                mode = "park"
                input_text = ""

            # If DEPART button is clicked
            if depart_btn.collidepoint(event.pos):
                active_input = True
                mode = "depart"
                input_text = ""

        # Handle keyboard input for license plate
        if event.type == pygame.KEYDOWN and active_input:

            # Press ENTER to confirm input
            if event.key == pygame.K_RETURN:

                # Call the appropriate stack operation
                if mode == "park":
                    message = garage.park(input_text)
                elif mode == "depart":
                    message = garage.depart(input_text)

                # Reset input state
                input_text = ""
                active_input = False

            # Remove last character
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            # Add typed character
            else:
                input_text += event.unicode

    # =========================
    # DRAW USER INTERFACE
    # =========================

    # Input field
    draw_text("License Plate:", 50, 40)
    draw_text(input_text, 200, 40, (255, 255, 0))

    # Buttons
    pygame.draw.rect(screen, (0, 150, 0), park_btn)
    pygame.draw.rect(screen, (150, 0, 0), depart_btn)

    draw_text("PARK VEHICLE", 680, 110)
    draw_text("DEPART VEHICLE", 665, 170)

    # Capacity display
    draw_text(f"Capacity: {garage.occupied} / {garage.garage_capacity}", 50, 80)

    # Garage display title
    draw_text("Garage (Top → Bottom)", 50, 120)
    pygame.draw.line(screen, (200, 200, 200), (50, 145), (550, 145), 2)

    # Display stack contents
    y = 160
    for vehicle in reversed(garage.stack):
        draw_text(
            f"{vehicle.plate} | Time In: {vehicle.arrival}",
            50,
            y
        )
        y += 30

    # Message area
    draw_text("MESSAGE:", 50, 520, (0, 200, 255))
    draw_text(message, 50, 550, (255, 255, 0))

    # Update screen
    pygame.display.flip()
    clock.tick(60)                             # Limit to 60 FPS

# Close pygame properly
pygame.quit()


