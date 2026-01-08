# Only use for terminal-based outputs
def clear_console():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_input(prompt, input_limit=None):

    # Checks if input_limit is provided
    if input_limit is None:
        input_limit = []
    else:
        input_limit = [str(response) for response in input_limit]

    # Loop until valid input is received. Empty inputs are not allowed.
    while True:
        try:
            user_input = input(prompt).strip()
            if user_input == "":
                print("Input cannot be empty. Please try again.")
            elif input_limit and user_input not in input_limit:
                print(f"Input must be one of the following: {', '.join(input_limit)}.")
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please try again.")