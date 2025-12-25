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
            
            if plate in parking_queue: # Check if the car is already parked
                print("This car is already parked.")
            else:
                parking_queue.append(plate) # Add the car to the queue
                print("Car parked successfully.")

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