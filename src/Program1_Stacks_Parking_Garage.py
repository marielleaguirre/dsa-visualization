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
import time
from datetime import datetime

pygame.init()                                  # Initialize pygame modules

WIDTH, HEIGHT = 900, 600                       # Window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parking Garage Stack Simulation")

font = pygame.font.Font(None, 28)              # Font for text
clock = pygame.time.Clock()                    # Controls frame rate


# This class acts as a blueprint for vehicles
class Vehicle:
    def __init__(self, plate):
        # Store the license plate number of the vehicle
        self.plate = plate
        
        # Record the time the vehicle enters the garage
        self.arrival = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Departure time is None while the vehicle is still parked
        self.departure = None

    def depart(self):
        # Record the time the vehicle leaves the garage
        self.departure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# This class manages the parking garage using a stack

class ParkingGarageStacks:
    def __init__(self):
        # Maximum number of vehicles allowed in the garage
        self.garage_capacity = 10
        
        # Stack to store Vehicle objects
        self.stack = []
        
        # Counter to track how many vehicles are parked
        self.occupied = 0

    def park(self, plate):
        # Check if the vehicle is already parked in the garage
        if plate in [vehicle.plate for vehicle in self.stack]:
            print(f"Vehicle {plate} is already parked.")
            time.sleep(1)
            return

        # Check if the garage has reached its capacity
        if self.occupied >= self.garage_capacity:
            print("Garage is FULL. Cannot park more vehicles.")
            time.sleep(1)
            return

        # Create a new Vehicle object using the blueprint
        vehicle = Vehicle(plate)

        # Push the vehicle onto the stack
        self.stack.append(vehicle)
        self.occupied += 1

        # Display parking confirmation
        print(f"Vehicle {vehicle.plate} parked at {vehicle.arrival}.")
        time.sleep(1)

    def depart(self, target_plate):
        # Inform the user that the system is searching for the vehicle
        print(f"Attempting to depart vehicle {target_plate}...")
        time.sleep(1)

        # Temporary stack to hold vehicles blocking the target vehicle
        temporary_stack = []
        found = False

        # Remove vehicles until the target vehicle is found
        while self.stack:
            vehicle = self.stack.pop()

            if vehicle.plate == target_plate:
                # Record the vehicle's departure time
                vehicle.depart()
                print(f"Vehicle {vehicle.plate} departed at {vehicle.departure}.")
                self.occupied -= 1
                found = True
                break
            else:
                # Store removed vehicles temporarily
                temporary_stack.append(vehicle)

        # If the target vehicle was not found in the garage
        if not found:
            print(f"Vehicle {target_plate} not found in the garage.")
            time.sleep(1)

        # Restore vehicles back to the main stack in correct order
        while temporary_stack:
            self.stack.append(temporary_stack.pop())

    def view_garage(self):
        # Check if the garage is empty
        if not self.stack:
            print("Garage is empty.")
            time.sleep(1)
            return

        # Display all vehicles currently parked
        print("\nGarage (Top → Bottom)")
        print("-" * 50)

        # Reverse stack to display top vehicle first
        for vehicle in reversed(self.stack):
            print(
                f"Vehicle {vehicle.plate} | "
                f"Time In: {vehicle.arrival} | "
                f"Time Out: {'Still Parked' if not vehicle.departure else vehicle.departure}"
            )
            time.sleep(1)


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



if __name__ == "__main__":
    main()