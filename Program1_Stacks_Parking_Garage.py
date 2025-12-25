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
        self.occupied = 0

    def park(self, car):            
        if self.occupied >= self.garage_capacity:        #Checks if the garage is full
          print("Garage is FULL. Cannot Park more cars.")
          time.sleep(1)
          return
        arrival_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        car = {
            "id": car,
            "arrival": arrival_time
        }
        self.stack.append(car)          #Inserting the car into the garage capacity
        self.occupied += 1
        print(f"Car {car['id']} parked at {car['arrival']}.")
        time.sleep(1)
        
    def depart(self, target_car):
        print(f"Attempting to depart car {target_car}...")
        time.sleep(2)
        temporary_stack = []            #Initialized temporary storage for storing cars temporarily

        while self.stack:                          #Used while loop for continouos checking for the target car
           recent_parked_car = self.stack.pop()           
           if recent_parked_car["id"] == target_car:
              print(f"Car {target_car} has departed the garage.")
              time.sleep(1) 
              self.occupied -= 1
              break
           temporary_stack.append(recent_parked_car)
        else:
           print("Cannot locate car")
           time.sleep(1)

        while temporary_stack:
           self.stack.append(temporary_stack.pop())        #This ensure that the order of the stack still remain.

    def view_garage(self):                            
        if not self.stack:
            print("Garage is empty.")
            time.sleep(1)
            return

        print("\nGarage (Top → Bottom):")
        for car in reversed(self.stack):
            print(
                f"Car {car['id']} | "
                f"Time In: {car['arrival']}")    #Display the currently parked cars
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
