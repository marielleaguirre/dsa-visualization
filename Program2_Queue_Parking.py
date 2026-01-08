import pygame                      # For graphics
import sys                         # For exiting program
from collections import deque      # Initialize the queue
from  datetime import datetime     # For timestamping

pygame.init()                      # Initialize pygame

# -------------------- WINDOW --------------------
WIDTH, HEIGHT = 1000, 700                           # Set window dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Create the window
pygame.display.set_caption("Queue Parking Garage")  # Set window title

CLOCK = pygame.time.Clock()                        # For controlling frame rate
FONT = pygame.font.SysFont("arial", 18)            # Set font for
BIG_FONT = pygame.font.SysFont("arial", 26)        # Set big font for titles

# -------------------- COLORS --------------------
BG = (25, 25, 25)                 # Background color (very dark gray)
GARAGE = (200, 200, 200)          # Garage color (light gray)
CAR_COLOR = (70, 160, 255)        # Car color (blue)
BTN = (90, 90, 90)                # Button color (dark gray)
BTN_HOVER = (130, 130, 130)       # Button hover color (medium gray)
WHITE = (255, 255, 255)           # White color
BLACK = (0, 0, 0)                 # Black color
RED = (220, 60, 60)               # Red color
GREEN = (60, 200, 120)            # Green color
INPUT_BG = (255, 255, 255)        # Input box background color (white)
INPUT_ACTIVE = (200, 230, 255)    # Input box active color (light blue)

# -------------------- GARAGE SETTINGS --------------------
CAPACITY = 5                       # Maximum number of cars in garage
SLOT_W = 130                       # Width of each parking slot
SLOT_H = 70                        # Height of each parking slot
START_X = 260                      # Starting X position for parking slots
START_Y = 320                      # Starting Y position for parking slots

# -------------------- MESSAGE SYSTEM --------------------
message_text = ""                  # Message text to display
message_color = GREEN              # Message color
message_time = 0                  # Time when message was set

def show_message(text, color=GREEN):                     # Function to show messages
    global message_text, message_color, message_time
    message_text = text                                  # Set the message text
    message_color = color                                # Set the message color
    message_time = pygame.time.get_ticks()               # Record the time the message was set

def draw_message():                                                                     # Function to draw messages
    if message_text and pygame.time.get_ticks() - message_time < 2000:                  # Show message for 2 seconds
        pygame.draw.rect(screen, message_color, (250, 10, 500, 40), border_radius=8)    # Draw message box
        msg = FONT.render(message_text, True, BLACK)                                    # Render the message text
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 22))                       # Center the message text

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
                return
        
        if len(self.queue) >= self.capacity:                       # Check if there is space in the garage
            print("Garage is FULL. Cannot park more cars.")        # Display full garage message
            return

        car = Car(plate_num)                                          # Create a new Car object
        self.queue.append(car)                                        # Add the car to the parking queue
        self.display()                                                # Display the updated garage status
        input("Car parked successfully! Press Enter to continue...")  # Confirmation message

    def depart(self):
        if not self.queue:                  # Check if there are any cars parked
            print("No cars to remove.")     # Display no cars message
            return

        car = self.queue.popleft()                             # Remove the first car in the queue
        car.time_out = datetime.now().strftime("%H:%M:%S")     # Record the time out
        self.departed.append(car)                              # Add the car to the departed list
        self.display()                                         # Display the updated garage status
        input("\nCar departed. Press ENTER to continue...")    # Confirmation message

    def table(self):                                                                # Display parking records
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
        print("Exiting the program... Thank you!")
        break

    else:
        print("Invalid choice. Try again.")
