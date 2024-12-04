# ElPsychicMustache
# 2024-11-24

# Moving the column renaming and column removing, as well as dtype changing methods to it's own class.

import pandas as pd

from .utilities import prompt_selection_for_column_list, prompt_for_columns_to_rename, prompt_user_for_int
from .validate_input import get_user_confirmation

class ColumnHandler:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe

    def remove_columns_interactively(self) -> None:
        """Provides the user a way to interactively delete columns from the dataframe.
        """
    
        user_wants_to_remove_columns: bool = get_user_confirmation(message="[*] Would you like to remove any columns? [Y/n]: ", true_options=["y", "yes", ""], false_options=["n", "no"])

        columns_to_remove: list[str] = []
        if user_wants_to_remove_columns:
            columns_to_remove = prompt_selection_for_column_list(message="[*] Please enter the numbers next to each column that you would like to remove. Leave blank to ignore.", list_of_options=self._dataframe.columns, default_all=False)

        if columns_to_remove:    
            print(f"[!] Removing the following columns: {columns_to_remove}")
            self._dataframe = self._dataframe.drop(columns=columns_to_remove)
            print(f"[+] Columns removed!")
        else:
            print("[-] No columns removed!")

    def rename_columns_interactively(self) -> None:
        """Provides the user a way to interactively rename the columns.
        """

        user_wants_to_rename = get_user_confirmation(message="[*] Would you like to rename any columns? [Y/n]: ", true_options=["yes", "y", ""], false_options=["no", "n"])

        columns_to_rename: list[str] = []
        if user_wants_to_rename:
            # TODO: update prompt_selection_for_column_list to dynamically inform user what the default for leaving blank is.
            columns_to_rename = prompt_selection_for_column_list(message="[*] Please enter the numbers next to each column that you would like to rename. Leave blank to select all columns.", list_of_options=self._dataframe.columns)

        rename_dict: dict[str, str] = {}
        if columns_to_rename:
            rename_dict = prompt_for_columns_to_rename(columns_to_rename)

        if columns_to_rename:
            print(f"[!] Renaming the following columns: {rename_dict.keys()}")
            self._dataframe = self._dataframe.rename(columns=rename_dict)
            print(f"[+] Columns have been renamed.")
        else:
            print("[-] No columns renamed!")

    def analyze_dtypes(self) -> None:
        self._explain_dtypes()
        print()
        if get_user_confirmation(
            message="[*] Would you like to change any d-types? [y/N] ", 
            true_options=["y", "yes"], 
            false_options=["n", "no", ""]
            ):

            columns_to_update: list[str] = prompt_selection_for_column_list(message="[*] Please enter the numbers next to each column that you would like to change the d-type. Leaving blank skips this step.", list_of_options=self._dataframe.columns, default_all=False)
            self._ask_new_dtypes(columns=columns_to_update)
    
    def _explain_dtypes(self):
        """Prints the column names and dtypes.
        """
        print(f"======= Columns and dtypes ======= \nThe dataframe's column names and types are the following: \n{self._dataframe.dtypes}")
    

    def _ask_new_dtypes(self, columns:list[str]):

        if not columns:
            return 
        
        options: dict[int, str] = {
            0: "Do nothing",
            1: "Change to datetime",
            2: "Change to numeric",
            3: "Change to categorical"
        }

        print()
        for column in columns:
            change_to_value = prompt_user_for_int(message=f"[*] What would you like to do with column {column}?", options=options)
            
            if change_to_value == 0:
                print("[!] Doing nothing.")
                pass
            elif change_to_value == 1:
                self._change_column_to_datetime(column_name=column)
            elif change_to_value == 2:
                self._change_column_to_numeric(column_name=column)
            elif change_to_value == 3:
                self._change_column_to_categorical(column_name=column)
            
    def _change_column_to_datetime(self, column_name:str) -> None:
        self._dataframe[column_name] = pd.to_datetime(self._dataframe[column_name])
    def _change_column_to_numeric(self, column_name:str, numeric_type:str) -> None:
        self._dataframe[column_name] = pd.to_numeric(self._dataframe[column_name])
    def _change_column_to_categorical(self, column_name:str) -> None:
        self._dataframe[column_name] = pd.Categorical(self._dataframe[column_name])

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe