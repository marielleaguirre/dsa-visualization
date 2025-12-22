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
        
    def depart(self, car):
        if not self.stack:                #Checks if the garage is empty
          self.stack.pop(car)               #Removing the car from the garage capacity
     
    def view_car():
        pass
    
    

