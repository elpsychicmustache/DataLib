# ElPsychicMustache
# 2024-11-04

def get_user_confirmation(message: str, true_options: list[str], false_options: list[str]) -> bool:
    """An infinite loop that repeats that returns true or false based on the user input. User input is casted as str.lower()

    Args:
        message (str): The message to display to the user.
        true_options (list[str]): The options that evaluate to true. MUST BE LOWER CASE
        false_options (list[str]): The options that evaluate to false. MUST BE LOWER CASE

    Returns:
        bool: True or False depending on which list the user input was found.
    """
    while True:
        try:
            user_input = input(message).lower()

            if user_input in true_options:
                return True
            elif user_input in false_options:
                return False
            else:
                raise ValueError(f"[-] {user_input} is not a valid choice!")
            
        except ValueError as e:
            print(f"{e}")
                

def validate_argument(valid_arg_options: list[str], user_input: str, parameter_name: str):
    """Checks if the argument for a parameter is valid based on a given list of values.

    Args:
        valid_arg_options (list[str]): List of acceptable values for the argument.
        user_input (str): The value submitted by user.
        parameter_name (str): The name of the parameter - used for error message.

    Raises:
        ValueError: If user_input is not found in valid_arg_options
    """
    if user_input not in valid_arg_options:
        raise ValueError(f"Invalid value for '{parameter_name}'. Expected one of {valid_arg_options}, but got '{user_input}'.")
    