<<<<<<< HEAD
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
import sys
from datetime import datetime

# ===================== STACK LOGIC =====================
class ParkingGarageStacks:
    def __init__(self):
        self.garage_capacity = 10       # The capacity of the garage
        self.stack = []                 # Set a variable into an empty list
        self.occupied = 0               # Counter for occupied slots

    def park(self, car_id):
        if self.occupied >= self.garage_capacity:    # Checks if the garage is full
            return None

        arrival_time = datetime.now().strftime("%H:%M:%S")
        car = {"id": car_id, "arrival": arrival_time}
        self.stack.append(car)           # Inserting the car into the garage stack
        self.occupied += 1
        return car

    def remove_top(self):
        if self.stack:
            self.occupied -= 1
            return self.stack.pop()
        return None


# ===================== PYGAME SETUP =====================
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Parking Garage (Stack)")

FONT = pygame.font.SysFont("arial", 18)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)
RED = (220, 80, 80)

SLOT_W, SLOT_H = 320, 40
BASE_X = 200
BASE_Y = 500


# ===================== CAR SPRITE =====================
class CarSprite:
    def __init__(self, car, x, y):
        self.car = car
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.speed = 8

    def update(self):
        if self.x < self.target_x:
            self.x += self.speed
        if self.x > self.target_x:
            self.x -= self.speed
        if self.y < self.target_y:
            self.y += self.speed
        if self.y > self.target_y:
            self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, SLOT_W, SLOT_H))
        text = FONT.render(
            f"{self.car['id']} | {self.car['arrival']}", True, BLACK
        )
        screen.blit(text, (self.x + 10, self.y + 10))

    def is_at_target(self):
        return self.x == self.target_x and self.y == self.target_y


# ===================== MAIN =====================
garage = ParkingGarageStacks()
sprites = []
input_text = ""
mode = None
message = ""

def get_slot_position(index):
    return BASE_X, BASE_Y - index * SLOT_H


running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Draw slots
    for i in range(garage.garage_capacity):
        x, y = get_slot_position(i)
        pygame.draw.rect(screen, GRAY, (x, y, SLOT_W, SLOT_H), 2)

    # Draw & update cars
    for sprite in sprites:
        sprite.update()
        sprite.draw()

    # UI text
    screen.blit(FONT.render("P - Park | D - Depart | ESC - Exit", True, BLACK), (520, 150))
    screen.blit(FONT.render(f"Input: {input_text}", True, BLACK), (520, 300))
    screen.blit(FONT.render(message, True, RED), (520, 340))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_p:
                mode = "PARK"
                input_text = ""
                message = "Enter plate number to PARK"

            elif event.key == pygame.K_d:
                mode = "DEPART"
                input_text = ""
                message = "Enter plate number to DEPART"

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            elif event.key == pygame.K_RETURN:
                if mode == "PARK":
                    car = garage.park(input_text)
                    if car:
                        x, y = -350, BASE_Y
                        sprite = CarSprite(car, x, y)
                        tx, ty = get_slot_position(len(sprites))
                        sprite.target_x, sprite.target_y = tx, ty
                        sprites.append(sprite)
                        message = "Car parked."
                    else:
                        message = "Garage FULL!"

                elif mode == "DEPART":
                    # Only top car can be animated simply
                    if sprites and sprites[-1].car["id"] == input_text:
                        sprite = sprites.pop()
                        sprite.target_x = WIDTH + 100
                        while not sprite.is_at_target():
                            sprite.update()
                            screen.fill(WHITE)
                            for s in sprites:
                                s.draw()
                            pygame.display.flip()
                            clock.tick(60)
                        garage.remove_top()
                        message = "Car departed."
                    else:
                        message = "Only TOP car can depart (Stack Rule)"

                input_text = ""
                mode = None

            else:
                input_text += event.unicode

pygame.quit()
sys.exit()
=======
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
import time
from datetime import datetime


class ParkingGarageStacks:
    def __init__(self):
        self.garage_capacity = 10       #The capacity of the garage
        self.stack = []                 #Set a variable into an empty list
        self.occupied = 0               #Counter for occupied slots

    def park(self, car):
        if car in [c["id"] for c in self.stack]:  #Check if the car is already parked
            print(f"Car {car} is already parked in the garage.")
            time.sleep(1)
            return
        
        if self.occupied >= self.garage_capacity:    #Checks if the garage is full
            print("Garage is FULL. Cannot park more cars.")
            time.sleep(1)
            return

        arrival_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #Record arrival time

        car = {
            "id": car,
            "arrival": arrival_time,
            "departure": None            #Stores departure time (None means still parked)
        }

        self.stack.append(car)           #Inserting the car into the garage stack
        self.occupied += 1
        print(f"Car {car['id']} parked at {car['arrival']}.")
        time.sleep(1)

    def depart(self, target_car):
        print(f"Attempting to depart car {target_car}...")
        time.sleep(2)

        temporary_stack = []             #Initialized temporary storage for storing cars temporarily
        found = False                    #Flag to check if the car is found

        while self.stack:                #Used while loop for continuous checking for the target car
            recent_parked_car = self.stack.pop()

            if recent_parked_car["id"] == target_car:
                recent_parked_car["departure"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Car {target_car} has departed the garage at {recent_parked_car['departure']}.")
                time.sleep(1)
                self.occupied -= 1
                found = True
                break
            else:
                temporary_stack.append(recent_parked_car)

        if not found:
            print(f"Car {target_car} not found in the garage.")
            time.sleep(1)

        while temporary_stack:
            self.stack.append(temporary_stack.pop())   # This ensures that the order of the stack still remains

    def view_garage(self):
        if not self.stack:
            print("Garage is empty.")
            time.sleep(1)
            return

        print("\nGarage (Top → Bottom):")
        print("-" * 40)

        for car in reversed(self.stack):
            print(
                f"Car {car['id']} | "
                f"Time In: {car['arrival']} | "
                f"Time Out: {'Still Parked' if not car['departure'] else car['departure']}"
            )                                           # Display the currently parked cars
            time.sleep(1)


def main():
    parking_garage = ParkingGarageStacks()

    while True:
        print("\n===== PARKING GARAGE MENU =====")
        time.sleep(1)

        print("1. Park a car")
        print("2. Depart a car")
        print("3. View Parking Garage")
        print("4. Exit")

        time.sleep(1)
        choice = input("Enter your choice (1-4): ")
        time.sleep(1)

        if choice == "1":
            car = input("Enter License Plate Number: ")
            parking_garage.park(car)
            time.sleep(1)

        elif choice == "2":
            car = input("Enter License Plate Number: ")
            parking_garage.depart(car)
            time.sleep(1)

        elif choice == "3":
            parking_garage.view_garage()
            time.sleep(1)

        elif choice == "4":
            print("\n👋 Exiting program. Thank you!")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()
>>>>>>> 34f1d0efbdffff6222672e645629f324bd1c41cf
