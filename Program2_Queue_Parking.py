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

        car = self.queue.popleft()                             # Remove the first car in the queue
        car.time_out = datetime.now().strftime("%H:%M:%S")     # Record the time out
        self.departed.append(car)                              # Add the car to the departed list
        self.display()                                         # Display the updated garage status
        input("\nCar departed. Press ENTER to continue...")    # Confirmation message

    def table(self):                                                                # Display parking records
        clear_screen()
        print("PARKING RECORD TABLE")
        print("-" * 60)                                                             # Divider line
        print(f"{'Plate Number':<15}{'Arrival':<15}{'Departure':<15}{'Status'}")    # Table column headers
        print("-" * 60)                                                             # Divider line

        for i, car in enumerate(self.queue, start=1):
            print(f"{car.plate_num:<15}{car.time_in:<15}{'-':<15}Slot {i}")           # Display parked cars

        for car in self.departed:
            print(f"{car.plate_num:<15}{car.time_in:<15}{car.time_out:<15}DEPARTED")  # Display departed cars
        
        print("-" * 60)
        input("\nPress ENTER to return to the menu...")  # Pause before returning to menu

# Main Program
garage = ParkingGarage(capacity=5)  # Set garage capacity

# Create the display menu
while True:
    print("QUEUE PARKING GARAGE MENU")
    print("1. Park a car")
    print("2. Remove a car")
    print("3. View Parking Table")
    print("4. Exit") 

# Ask the user to choose an option
    choice = input("\nChoose an option (1-4): ")

    if choice == "1":  # Park a car
        plate_num = input("Enter Plate Number: ")
        garage.arrive(plate_num)

    elif choice == "2": # Remove a car
        garage.depart()

    elif choice == "3": # View Parking Table
        garage.table()
    
    elif choice == "4": # Exit the program
        clear_screen()
        print("Exiting the program... Thank you!")
        time.sleep(1)
        break

    else:
        print("Invalid choice. Try again.")
        time.sleep(1)