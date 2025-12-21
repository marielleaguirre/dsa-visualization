'''
Binary Search Tree Pseudocode:
1. Display a menu to choose input method:
    a. Random input
    b. User input
2. Ask the user to enter the number of nodes (between 10 and 30)
3. If the user chooses Random input:
    a. Generate n random integers
4. If the user chooses User input:
    a. Prompt the user to enter n integers
5. Create an empty Binary Search Tree (BST)
6. For each number in the list:
    a. Insert the number into the BST following rules:
        i. If BST is empty, create root node
        ii. If number <= current node value, go to left node
        iii. If number > current node value, go to right node
        iv. Repeat until correct position is found
7. Display the list of numbers entered/generated
8. Perform and display the following traversals:
    a. Inorder Traversal (Left → Top → Right)
    b. Preorder Traversal (Top → Left → Right)
    c. Postorder Traversal (Left → Right → Top)
'''