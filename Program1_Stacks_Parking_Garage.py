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

class ParkingGarageStacks:
    def __init__(self):
        self.garage_capacity = 10       #The capacity of the garage
        self.stack = []                 #Set a variable into an empty list
        self.occupied = 0

    def park(self, car):
        self.occupied += 1              
        if self.occupied >= self.garage_capacity:        #Checks if the garage is full
          print("Garage is FULL. Cannot Park more cars.")
          return
        else:
          self.stack.append(car)          #Inserting the car into the garage capacity
        
    def depart(self, target_car):
        temporary_stack = []            #Initialized temporary storage for storing cars temporarily

        while self.stack:                          #Used while loop for continouos checking for the target car
           recent_parked_car = self.stack.pop()           
           if recent_parked_car == target_car:
              print(f"Car {target_car} has departed the garage.")
              self.occupied -= 1
              break
           temporary_stack.append(recent_parked_car)
        else:
           print("Cannot locate car")

        while temporary_stack:
           self.stack.append(temporary_stack.pop())        #This ensure that the order of the stack still remain.

    def view_garage(self):                            
        if not self.garage:
            print("Garage is empty.")
            return

        print("\nGarage (Top → Bottom):")
        for car in reversed(self.garage):
            print(
                f"Car {car['id']} | "
                f"Time In: {car['time_in'].strftime('%Y-%m-%d %H:%M:%S')}"  #Display the currently parked cars 
            )

def main():
    parking_garage = ParkingGarageStacks()

    while True:
        print("\n===== PARKING GARAGE MENU =====")
        print("1. Park a car")
        print("2. Depart a car")
        print("3. View Parking Garage")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            car = input("Enter License Plate Number: ")
            parking_garage.park(car)

        elif choice == "2":
            car = input("Enter License Plate Number: ")
            parking_garage.depart(car)

        elif choice == "3":
            parking_garage.view_garage()

        elif choice == "4":
            print("\n👋 Exiting program. Thank you!")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
