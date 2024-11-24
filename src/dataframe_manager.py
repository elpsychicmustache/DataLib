# Name: dataframe_manager
# Author: ElPsychicMustache
# Created: 2024-11-04

# Code is a work in progress based on teachings of Rob Mulla https://youtu.be/xi0vhXFPegw?si=cicV7Pdf9NTjYBRC

import pandas as pd
import seaborn as sns

from .duplicate_analyzer import DuplicateAnalyzer
from .feature_analyzer import FeatureAnalyzer
from .null_analyzer import NullAnalyzer

from .utilities import get_df_from_csv, prompt_selection_for_column_list, prompt_for_columns_to_rename, prompt_user_for_int
from .validate_input import get_user_confirmation, validate_argument


# TODO: Add a pause between each step of prepare_data
class DataframeManager:

    def __init__(self, dataframe: pd.DataFrame=None, file_path: str="../data/input/", file_name: str="data.csv", date_columns: list[str]=None, column_names: list[str]=None) -> None:
        """Class used to hold a Pandas dataframe so that standardized analysis can be performed on it.

        Args:
            dataframe: (pd.DataFrame, optional): A pandas dataframe; else, pass file_path and/or file_name.
            file_path (str, optional): The path to the csv file. Defaults to "../data/input/".
            file_name (str, optional): The name of the csv file. Defaults to "data.csv".
            date_columns (list[str], optional): Columns that contain date information.. Defaults to None.
            column_names (list[str], optional): The names to provide each column. Defaults to None.
        """

        if dataframe:
            self._dataframe = dataframe
        else:
            self._dataframe: pd.DataFrame = get_df_from_csv(file_path, file_name, date_columns, column_names)
        
    def understand_data(self, head_tail_size: int=20, analysis_type="short") -> None:
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
        print("======= Null values in each column ======= ")
        print(f"{self._dataframe.isna().sum()}")
    # END OF COLLECTION OF SIMPLE PRINT FUNCTIONS


    def prepare_data(self, skip_remove:bool=False, skip_rename:bool=False, skip_dtypes:bool=False, skip_nulls:bool=False, skip_dups: bool=False, skip_reset:bool=False) -> None:
        """Step two of exploratory data anlalysis. Provides a suite of methods that allow a user to prepare the data for further anlaysis.

        Args:
            skip_remove (bool, optional): Skip the column removal step. Defaults to False.
            skip_rename (bool, optional): Skip the column rename step. Defaults to False.
            skip_dtypes (bool, optional): Skip the dtype analysis step. Defaults to False.
            skip_nulls (bool, optional): Skip the null aalysis step. Defaults to False.
            skip_dups (bool, optional): Skip the duplicate analysis step. Defaults to False.
            skip_reset (bool, optional): Skip the index reset step. Defaults to False.
        """

        # TODO: Validate argument types as bools using validate_input
        if not skip_remove:
            print("\n[!] Starting remove columns step:")
            self.remove_columns_interactively()
            print("[!] Remove columns step finished.")
        if not skip_rename:
            print("\n[!] Starting rename columns step:")
            self.rename_columns_interactively()
            print("[!] Rename columns step finished.")
        if not skip_dtypes:
            print("\n[!] Starting d-types step:")
            self.analyze_dtypes()
            self._explain_dtypes()
            print("[!] D-types step finished.")
        
        if not skip_nulls:
            print("\n[!] Starting null analysis step:")
            self.analyze_nulls()
            print("[!] Null step finished.")
        if not skip_dups:
            print("\n[!] Starting duplicate analysis step:")
            self.analyze_duplicates()
            print("[!] Duplicates step finished.")
        if not skip_reset:
            print("\n[!] Starting index reset step:")
            self._reset_index()
            print("[!] Index reset step complete!")
        
        print("\n[!] Data preparation step complete!")

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

    def analyze_duplicates(self) -> None:
        """Provides the user a way to analyze and handle the duplicate values of the dataframe.
        """

        duplicate_analyzer = DuplicateAnalyzer(self._dataframe)
        self._dataframe = duplicate_analyzer.dataframe
        del duplicate_analyzer
            
    def analyze_nulls(self) -> None:
        """Passes self.dataframe object into NullAnalyzer class which handles all the null analysis logic.
        This is to abstract some of the methods since it really polluted the DataframeManager class.
        """
        null_analyzer = NullAnalyzer(self._dataframe)
        self._dataframe = null_analyzer.dataframe
        del null_analyzer

    def _reset_index(self) -> None:
        """Allows the user to reset the index of the dataframe..
        """
        user_wants_index_rest: bool = get_user_confirmation(message="[*] Would you like to reset the index? [Y/n]", true_options=["yes", "y", ""], false_options=["no", "n"])
        if user_wants_index_rest:
            self._dataframe = self._dataframe.reset_index(drop=True)
            print("[+] Index has been reset!")
        else:
            print("[-] Index has not been reset.")

    def understand_features(self):
        print("[!] Beginning feature understanding (univariate) analysis step!")
        feature_analyzer = FeatureAnalyzer(self._dataframe)
        del feature_analyzer
            
    def __str__(self) -> str:
        return f"This is a pandas DataFrame object. Here are the first 25 rows: {self._dataframe.head(25)}"

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
