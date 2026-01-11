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


# =========================
# PARKING GARAGE STACK CLASS
# =========================
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

# Main function to run the parking garage program

def main():
    # Create an instance of the parking garage
    parking_garage = ParkingGarageStacks()

    # Loop until the user chooses to exit
    while True:
        print("\n===== PARKING GARAGE MENU =====")
        print("1. Park a vehicle")
        print("2. Depart a vehicle")
        print("3. View Parking Garage")
        print("4. Exit")

        # Ask the user for a menu choice
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            plate = input("Enter License Plate Number: ")
            parking_garage.park(plate)

        elif choice == "2":
            plate = input("Enter License Plate Number: ")
            parking_garage.depart(plate)

        elif choice == "3":
            parking_garage.view_garage()

        elif choice == "4":
            print("\n👋 Exiting program. Thank you!")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")

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

if __name__ == "__main__":
    main()