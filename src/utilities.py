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
    """_summary_

    Args:
        message (str): The message to display to the user.
        list_of_options (list[str]): The list of options the user can choose from.
        default_all (bool, optional): If the user does nothing, return all options or return no options. Defaults to True.

    Returns:
        list[str]: The options the user chose.
    """

    selection_list: list[int] = []
    option_dict: dict[int, str] = {i: list_of_options[i] for i in range(len(list_of_options))}

    for (key, value) in option_dict.items():
        print(f"{key}: {value}")
    
    # TODO: move to validate_input
    print(message)
    user_selection_str = str(input("Numbers should be separated by spaces. Leave blank to select all columns: "))
    if user_selection_str == "":
        user_selection_list = []
    else:
        user_selection_list: list[int] = user_selection_str.split(" ")

    if user_selection_list:
        for selection in user_selection_list:
            selection_list.append(option_dict[int(selection)])
        return selection_list
    else:
        if default_all:
            return list(option_dict.values())
        else:
            return []
    

def prompt_for_columns_to_rename(list_of_rename_items: list[str]) -> dict[str, str]:
    columns_to_rename: dict[str, str] = {}

    for column in list_of_rename_items:
        new_column_name = str(input(f"[*] Rename column {column} to (leave blank to ignore change): ")).strip()

        if new_column_name != "":
            columns_to_rename[column] = new_column_name

    return columns_to_rename