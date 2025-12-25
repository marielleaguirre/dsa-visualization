'''
Queue Parking Garage Similation Pseudocode:
1. Create a menu with options to:
    a. Park a car
    b. Remove a car
    c. View parked cars
    d. Exit the program
2. Ask the user to select an option from the menu.
3. If the user selects "Park a car":
    a. Check if there is available space in the parking garage.
    b. If space is available, prompt the user to enter the car's license plate number.
    c. Add the car to the parking queue.
    d. Confirm that the car has been parked.
4. If the user selects "Remove a car":
    a. Check if there are any cars parked in the garage.
    b. If there are parked cars, remove the car in first slot from the parking queue.
    c. Confirm that the car has been removed.
5. If the user selects "View parked cars":
    a. Display a list of all parked cars.
6. If the user selects "Exit":
    a. End the program.
'''

import time                        # For simulating delays
import os                          # For clearing the console
from collections import deque      # Initialize the queue
from  datetime import datetime     # For timestamping

def clear_screen():                                         # Clear the console screen
    os.system("cls" if os.name == "nt" else "clear")        # depending on OS

class Car:                                                       # Created a blueprint for Car
    def __init__(self, plate_num):                               
        self.plate_num = plate_num                               # Stores car's plate number
        self.time_in = datetime.now().strftime("%H:%M:%S")       # Records current time as time in with format HH:MM:SS
        self.time_out = None

class ParkingGarage:                              # Created a blueprint for Parking Garage
    def __init__(self, capacity):                               
        self.capacity = capacity                  # Sets the capacity of the parking garage
        self.queue = deque()                      # Initializes an empty queue to store parked cars
        self.departed = []                        # List to store departed cars
    
    def display(self):                          # Display the parking garage header
        clear_screen()                          # Clears the terminal screen before displaying
        print("QUEUE PARKING GARAGE")           
        print("=" * 40)                         # Divider line

        if not self.queue:
            print("\n   [EMPTY]\n")                             # If no cars are parked, display [EMPTY]
        else:
            for i, car in enumerate(self.queue):
                print(f" | Slot {i+1}: {car.plate_num}")        # Display the slot and plate number
                print(" |------------------------------")       # Separator for slots

        print("=" * 40)                                             # Divider line
        print(f"Parked Cars: {len(self.queue)}/{self.capacity}")    # Display current occupancy
        print(f"Departed Cars: {len(self.departed)}")               # Display number of departed cars

    def arrive(self, plate_num):
        for car in self.queue:
            if car.plate_num == plate_num:                                  # Check for duplicate plate numbers
                print(f"ERROR: Plate '{plate_num}' is already parked!")     # Display error message
                time.sleep(2)                                               # Pause for 2 seconds                                 
                return
        
        if len(self.queue) >= self.capacity:                       # Check if there is space in the garage
            clear_screen()
            print("Garage is FULL. Cannot park more cars.")        # Display full garage message
            time.sleep(2)
            return

        car = Car(plate_num)                                          # Create a new Car object
        self.queue.append(car)                                        # Add the car to the parking queue
        self.display()                                                # Display the updated garage status
        input("Car parked successfully! Press Enter to continue...")  # Confirmation message

    def depart(self):
        if not self.queue:                  # Check if there are any cars parked
            clear_screen()
            print("No cars to remove.")     # Display no cars message
            time.sleep(2)
            return


parking_queue = deque()
capacity = 5  # Set the capacity of the parking garage

# Create the display menu
while True:
    print("\nParking Garage Menu:")
    print("1. Park a car")
    print("2. Remove a car")
    print("3. View parked cars")
    print("4. Exit") 

# Ask the user to choose an option
    choice = input("Choose an option (1-4): ")

    if choice == "1": # Park a car
        if len(parking_queue) >= capacity: # If the garage is full
            print("Garage is full.")
        else:
            plate = input("Enter the car's license plate number: ")

    elif choice == "2": # Remove a car
        if not parking_queue: # If there are no cars parked
            print("No cars to remove.")
        else:
            removed_car = parking_queue.popleft() # Remove the first car in the queue
            print(f"Car with license plate {removed_car} has been removed.")

    elif choice == "3": # View parked cars
        if not parking_queue: # If there are no cars parked
            print("No cars are currently parked.")
        else:
            print("Parked cars:")
            for car in parking_queue:
                print(car)
    
    elif choice == "4": # Exit the program
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Try again.")