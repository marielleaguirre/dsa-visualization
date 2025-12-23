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
          pass
        else:
          self.stack.append(car)          #Inserting the car into the garage capacity
        
    def depart(self, target_car):
        temporary_stack = []            #Initialized temporary storage for storing cars temporarily

        while self.stack:                          #Used while loop for continouos checking for the target car
           recent_parked_car = self.stack.pop()           
           if recent_parked_car == target_car:
              break
           temporary_stack.append(recent_parked_car)
        else:
           print("Cannot locate car")

    def view_car():
        pass
    
    

