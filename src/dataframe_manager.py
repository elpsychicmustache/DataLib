# PsychicMustache
# 2024-11-04 Created

# Code is a work in progress based on teachings of Rob Mulla https://youtu.be/xi0vhXFPegw?si=cicV7Pdf9NTjYBRC

import pandas as pd

from .validate_input import get_user_confirmation, validate_argument
from .utilities import get_df_from_csv

class DataframeManager:

    def __init__(self, file_path: str="../data/input/", file_name: str="data.csv", date_columns: list[str]=None, column_names: list[str]=None) -> None:
        """Class used to hold a Pandas dataframe so that standardized analysis can be performed on it.

        Args:
            file_path (str, optional): The path to the csv file. Defaults to "../data/input/".
            file_name (str, optional): The name of the csv file. Defaults to "data.csv".
            date_columns (list[str], optional): Columns that contain date information.. Defaults to None.
            column_names (list[str], optional): The names to provide each column. Defaults to None.
        """
        self._dataframe: pd.DataFrame = get_df_from_csv(file_path, file_name, date_columns, column_names)


    def understand_data(self, head_tail_size: int = 20, analysis_type="short") -> None:
        """Step one of Exploratory data anlysis. Prints some information to help understand the dataframe.

        Args:
            head_tail_size (int, optional): The number of rows to show for head and tail function. Defaults to 20.
            analysis_type (str, optional): Can be "short" or "long". Changes the amount of detail shown about the dataframe. Defaults to "short".
        """

        validate_argument(valid_arg_options=["short", "long"], user_input=analysis_type, parameter_name="analysis_type")

        self._explain_shape()
        self._explain_dtypes()
        self._show_descriptive_stats()
        self._show_head_tail()

        if analysis_type == "long":
            self._show_null_values()

    
    # COLLECTION OF SIMPLE PRINT FUNCTIONS
    def _explain_shape(self):
        """Prints the shape of the dataframe.
        """
        print(f"======= Dataframe shape ======= \nThe dataframe has {self._dataframe.shape[0]} rows and {self._dataframe.shape[1]} columns.")
    def _explain_dtypes(self):
        """Prints the column names and dtypes.
        """
        print(f"======= Columns and dtypes ======= \nThe dataframe's column names and types are the following: \n{self._dataframe.dtypes}")
    def _show_descriptive_stats(self):
        """Prints the descriptive stats of each column.
        """
        print(f"======= Descriptive stats ======= \n{self._dataframe.describe()}")
    def _show_head_tail(self, head_tail_size: int = 20):
        """Prints the head and tail of the dataframe.

        Args:
            head_tail_size (int, optional): How many rows to print for head and tail. Defaults to 20.
        """
        print(f"======= First {head_tail_size} rows ======= \n{self._dataframe.head(head_tail_size)}")
        print(f"\n======= Last {head_tail_size} rows ======= \n{self._dataframe.tail(head_tail_size)}")
    def _show_null_values(self):
        """Prints how many null values appear in each column.
        """
        print(f"\n======= Null values in each column ======= \n")
        for column in self._dataframe.columns:
            len(self._dataframe[column].loc[self._dataframe[column].isna()])
    # END OF COLLECTION OF SIMPLE PRINT FUNCTIONS

    def process_data(self, ignore_remove:bool=False, ignore_rename:bool=False) -> None:
        """Step two of Exploratory Data Analysis. Provides some generic function that help with processing data.
        """
        if not ignore_remove:
            self.remove_columns_interactively()
        if not ignore_rename:
            self.rename_columns_interactively()


    def remove_columns_interactively(self) -> None:
        """Provides the user a way to interactively delete columns from the dataframe.
        """
    
        user_wants_to_remove_columns: bool = get_user_confirmation(message="[*] Would you like to remove any columns? [Y/n]: ", true_options=["y", "yes", ""], false_options=["n", "no"])

        columns_to_remove: list[str] = []
        if user_wants_to_remove_columns:
            columns_to_remove = self._prompt_for_columns_to_remove()

        if columns_to_remove:    
            print(f"[!] Removing the following columns: {columns_to_remove}")
            self._dataframe = self._dataframe.drop(columns=columns_to_remove)
            print(f"[+] Columns removed!")
        else:
            print("[-] No columns removed!")


    def _prompt_for_columns_to_remove(self) -> list[str]:
        """Prompts the user each column name and asks if they want to remove them.

        Returns:
            list[str]: The list of columns to remove.
        """

        columns_to_remove: list[str] = []

        for column in self._dataframe.columns:
            remove_flag: bool = get_user_confirmation(message=f"[*] Remove column {column}? [y/N]: ", true_options=["y", "yes"], false_options=["n", "no", ""])

            if remove_flag:
                columns_to_remove.append(column)

        return columns_to_remove
    

    def rename_columns_interactively(self) -> None:
        """Provides the user a way to interactively rename the columns.
        """

        user_wants_to_rename = get_user_confirmation(message="[*] Would you like to rename any columns? [Y/n]: ", true_options=["yes", "y", ""], false_options=["no", "n"])

        columns_to_rename: dict[str, str] = {}
        if user_wants_to_rename:
            columns_to_rename = self._prompt_for_columns_to_rename()

        if columns_to_rename:
            print(f"[!] Renaming the following columns: {columns_to_rename.keys()}")
            self._dataframe = self._dataframe.rename(columns=columns_to_rename)
            print(f"[+] Columns have been renamed.")
        else:
            print("[-] No columns renamed!")


    def _prompt_for_columns_to_rename(self) -> dict[str, str]:
        """Prompts the user a way to interactively rename the columns of the dataframe.

        Returns:
            dict[str, str]: Dictionary containing the original column name as the key and the value as the new column name.
        """

        columns_to_rename: dict[str, str] = {}

        for column in self._dataframe.columns:
            new_column_name = str(input(f"[*] Rename column {column} to (leave blank to ignore change): ")).strip()

            if new_column_name != "":
                columns_to_rename[column] = new_column_name

        return columns_to_rename


    def __str__(self) -> str:
        return f"This is a pandas DataFrame object. Here are the first 25 rows: {self._dataframe.head(25)}"

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
