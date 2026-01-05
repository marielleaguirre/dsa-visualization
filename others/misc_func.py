class ValidateInput:

    def validate(prompt, input_limit=[]):
        while True:
            try:
                user_input = input(prompt).strip()

                if user_input in input_limit or input_limit == []:
                    return user_input

            except ValueError:
                print("Invalid Input!")