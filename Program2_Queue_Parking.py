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

# Initialize the queue
from collections import deque

parking_queue = deque()
capacity = 5  # Set the capacity of the parking garage

# Create the display menu
while True:
    print("\nParking Garage Menu:")
    print("1. Park a car")
    print("2. Remove a car")
    print("3. View parked cars")
    print("4. Exit") 