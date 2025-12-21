'''
Recursion(Tower of Hanoi) Pseudocode:
1. Ask the user to enter the number of disks.
2. Define a recursive function `tower_of_hanoi(n, source, auxiliary, target)`:
    a. If n == 1:
        i. Print "Move disk 1 from source to target"
        ii. Return
    b. Move n-1 disks from source to auxiliary using target as auxiliary
    c. Print "Move disk n from source to target"
    d. Move n-1 disks from auxiliary to target using source as auxiliary
3. Call `tower_of_hanoi` with the number of disks, source = A, auxiliary = B, target = C
'''