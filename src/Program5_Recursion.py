def tower_of_hanoi(num_disks, source, auxiliary, target):
    if num_disks == 1:
        print(f"Move disk 1 from {source} to {target}")  # Base case: move one disk directly to target
        return
    tower_of_hanoi(num_disks - 1, source, target, auxiliary)  # Move n-1 disks from source to auxiliary
    print(f"Move disk {num_disks} from {source} to {target}")  # Move the largest disk to target
    tower_of_hanoi(num_disks - 1, auxiliary, source, target)  # Move n-1 disks from auxiliary to target

def main():
    print("Recursion: Tower of Hanoi")
    while True:
        try:
            num_disks = int(input("Enter the number of disks (1-7): "))
            if 1 <= num_disks <= 7:  # Check if the number of disks is within the allowed range (1-7)
                break
            else:      
                print("Invalid. Please enter a valid number between 1 and 7.")
        except ValueError:  # Handles non-integer inputs
            print("Invalid input. Enter an integer.")

    print(f"\nMoves to solve Tower of Hanoi with {num_disks} disks:")
    tower_of_hanoi(num_disks, 'A', 'B', 'C')

main()