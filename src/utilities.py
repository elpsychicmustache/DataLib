# Name: utilities
# Author: ElPsychicMustache
# Created: 2024-11-04

import pandas as pd


def get_df_from_csv(file_path: str, file_name: str, date_columns: list[str], column_names: list[str]) -> pd.DataFrame:
    
    # TODO: Move full_file_path to validate_input
    # making sure user did not forget to add '/' at the end of file path
    if file_path[-1] != '/':
        file_path += '/'

    full_file_path: str = f"{file_path}{file_name}"

    read_csv_kwargs: dict = {}

    if date_columns:
        read_csv_kwargs['parse_dates'] = date_columns
    if column_names:
        read_csv_kwargs['names'] = column_names

    return pd.read_csv(full_file_path, **read_csv_kwargs)


def prompt_selection_for_column_list(message: str, list_of_options: list[str], default_all: bool=True) -> list[str]:
    selection_list: list[int] = []
    option_dict: dict[int, str] = {i: list_of_options[i] for i in range(len(list_of_options))}

    show_options_to_user(message=message, option_dict=option_dict, default_all_flag=default_all)
    user_input = get_user_input_str(message="Enter options: ")
    selection_list = generate_list_from_input_str(user_input=user_input, option_dict=option_dict)

    if selection_list:
        return selection_list
    else:
        if default_all:
            return list_of_options
        else:
            return []
    

def show_options_to_user(message:str, option_dict:dict[str,str], default_all_flag:bool) -> None:
    output_message: str = ""
    output_message += message
    for (key, value) in option_dict.items():
        output_message += f"\n{key}: {value}"
    if default_all_flag:
        output_message += "\nNumbers should be separated by spaces. Leaving blank selects all."
    else:
        output_message += "\nNumbers should be separated by spaces. Leaving blank skips this."
    
    print(output_message)


def get_user_input_str(message:str) -> str:
    user_input = str(input(message))
    return user_input


def generate_list_from_input_str(user_input:str, option_dict:dict[str,str]) -> list[str]:
    if user_input.strip() == "":
        return []
    
    user_input_list: list[str] = user_input.strip().split(" ")
    selection_list = []
    for selection in user_input_list:
        try:
            selection_list.append(option_dict[int(selection)])
        except KeyError:
            raise KeyError(f"You entered an invalid option -> {selection}")
        except ValueError:
            raise ValueError(f"You entered an invalid option -> {selection}")
    return selection_list


def prompt_for_columns_to_rename(list_of_rename_items: list[str]) -> dict[str, str]:
    columns_to_rename: dict[str, str] = {}

    for column in list_of_rename_items:
        new_column_name: str = get_user_input_str(message=f"[*] Rename column {column} to (leave blank to ignore change): ").strip()
        new_column_name = new_column_name.strip()
        if new_column_name != "":
            columns_to_rename[column] = new_column_name

    return columns_to_rename


def prompt_user_for_int(message: str, options: dict[int, str]) -> int:

    print(message)
    for key, value in options.items():
        print(f"{key}: {value}")
    
    user_input: int = int(input())

    if user_input in options:
        return user_input
    else:
        raise ValueError(f"{user_input} is not a valid option from {list(options.keys())}")  # casting as list is needed for proper output