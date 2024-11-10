# Name: dataframe_manager
# Author: ElPsychicMustache
# Created: 2024-11-04

# Code is a work in progress based on teachings of Rob Mulla https://youtu.be/xi0vhXFPegw?si=cicV7Pdf9NTjYBRC

import pandas as pd

from .validate_input import get_user_confirmation, validate_argument
from .utilities import get_df_from_csv, prompt_selection_for_column_list, prompt_for_columns_to_rename


class DataframeManager:

    def __init__(self, dataframe: pd.DataFrame=None, file_path: str="../data/input/", file_name: str="data.csv", date_columns: list[str]=None, column_names: list[str]=None) -> None:
        """Class used to hold a Pandas dataframe so that standardized analysis can be performed on it.

        Args:
            file_path (str, optional): The path to the csv file. Defaults to "../data/input/".
            file_name (str, optional): The name of the csv file. Defaults to "data.csv".
            date_columns (list[str], optional): Columns that contain date information.. Defaults to None.
            column_names (list[str], optional): The names to provide each column. Defaults to None.
        """

        if dataframe:
            self._dataframe = dataframe
        else:
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
        print("======= Null values in each column ======= \n")
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
        if not skip_rename:
            print("\n[!] Starting rename columns step:")
            self.rename_columns_interactively()
        if not skip_dtypes:
            print("\n[!] Starting d-types step:")
            # TODO: Flesh out this step more.
            #   Show user columns and dtypes
            #   Ask if user wants to change any column's dtypes (mainly datetime, ints, or floats)
            self._explain_dtypes()
        
        if not skip_nulls:
            print("\n[!] Starting null analysis step:")
            self.analyze_nulls()
        if not skip_dups:
            print("\n[!] Starting duplicate analysis step:")
            self.analyze_duplicates()
        if not skip_reset:
            print("\n[!] Starting index reset step:")
            self._reset_index()
        
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
    
    def analyze_duplicates(self) -> None:
        """Provides the user a way to analyze and handle the duplicate values of the dataframe.
        """

        user_wants_to_analyze_duplicates: bool = get_user_confirmation(message="[*] Would you like to analyze duplicates? [Y/n]: ", true_options=["yes", "y", ""], false_options=["no", "n"])
        
        if not user_wants_to_analyze_duplicates:
            print("[-] Duplicate analysis step skipped.")
            return
        
        subset_for_dup_identification: list[str] = prompt_selection_for_column_list(message="[*] Please enter the numbers next to each column to use as subsets to find duplicates.", list_of_options=self._dataframe.columns)

        print(f"[!] Looking for duplicates in columns: {subset_for_dup_identification} ...")
        duplicate_rows = self._return_duplicates(subset_for_dup_identification)

        if len(duplicate_rows) == 0:
            print("[!] There are no duplicates in this dataset with the selected subset_list.")
            return
        else:
            print(f"\n[!] {len(duplicate_rows)} duplicate rows identified. Here is a specific example of a duplicate: ")
            self._show_duplicate_example(subset_for_dup_identification, duplicate_rows)
        
        user_wants_to_remove_duplicates = get_user_confirmation(message="[*] Do you want to remove duplicates (first duplicate row is kept)? [y/N]", true_options=["y", "yes"], false_options=["n", "no", ""])
        if user_wants_to_remove_duplicates:
            self._remove_duplicates(subset_for_dup_identification)
            print("[!] Duplicates removed!")
        else:
            print("[!] Duplicates kept!")
            
    def _return_duplicates(self, subset_list: list[str]=None) -> pd.DataFrame:
        """Returns a dataframe with all duplicate rows identified.

        Args:
            subset_list (list[str], optional): The columns to consider duplicates. Defaults to None.

        Returns:
            pd.DataFrame: A dataframe consisting of only duplicate values.
        """
        return self._dataframe.loc[self._dataframe.duplicated(subset=subset_list, keep=False)]
    
    def _show_duplicate_example(self, duplicate_examples: pd.DataFrame, subset_list: list[str]=None) -> None:
        """Provides the user a simple example of duplicate rows from the dataframe.

        Args:
            subset_list (list[str]): The list of column names to consider duplicates. Default to None.
            duplicate_examples (pd.DataFrame): A dataframe consisting of duplicate values.
        """
        
        column_values: list[str] = [duplicate_examples.iloc[0][column] for column in subset_list]

        query_dict: dict[str, str] = dict(zip(subset_list, column_values))

        query_results: pd.DataFrame = duplicate_examples

        for column, value in query_dict.items():
            query_results = query_results[query_results[column] == value]

        print(query_results)

    def _remove_duplicates(self, subset_list: list[str]=None) -> None:
        """Removes duplicate values, keeping the first value.

        Args:
            subset_list (list[str]): The list of columns to consider duplicates. Defaults to None.
        """
        self._dataframe = self._dataframe.drop_duplicates(subset=subset_list, keep="first")

    def _reset_index(self) -> None:
        """Allows the user to reset the index of the dataframe..
        """
        user_wants_index_rest: bool = get_user_confirmation(message="[*] Would you like to reset the index? [Y/n]", true_options=["yes", "y", ""], false_options=["no", "n"])
        if user_wants_index_rest:
            self._dataframe = self._dataframe.reset_index(drop=True)
            print("[+] Index has been reset!")
        else:
            print("[-] Index has not been reset.")

    def analyze_nulls(self) -> None:
        # TODO: ask if user wants to remove (rows or simply column), impute (mean, median, mode, or forward-fill [or N/A for string data]), or do nothing
            
        user_wants_to_analyze_nulls = get_user_confirmation(message="[*] Would you like to analyze null values? [Y/n] ", true_options=["yes", "y", ""], false_options=["no", "n"])
        
        null_columns: list[str] = []
        if user_wants_to_analyze_nulls:
            self._show_null_values()
            null_columns = self._find_columns_with_nulls()

        print()  # making output a bit niver

        if null_columns:
            self._show_ratio_of_nulls(null_columns)

    def _find_columns_with_nulls(self) -> list[str]:
        """Provides a list of columns that contain null values.

        Returns:
            list[str]: List of columns that contain null values.
        """
        columns_with_nulls_series: pd.Series = self._dataframe.isnull().sum()
        columns_with_nulls: list[str] = list(columns_with_nulls_series.loc[columns_with_nulls_series != 0].index)

        return columns_with_nulls
    
    def _show_ratio_of_nulls(self, null_columns: list[str]) -> None:
        """Prints out each column, shows the % of rows that are null, and then provides a recommendation on what to do with the null values.

        Args:
            null_columns (list[str]): The list of columns that contain null values.
        """
        num_rows: int = self._dataframe.shape[0]

        print("======= Percentage of null values in each column =======")
        for column in null_columns:
            perc_null: float = self._dataframe[column].isnull().sum() / num_rows
            print(f"[!] {column} {'{:.2%}'.format(perc_null)} ", end="")
            self._determine_recommendation(self._dataframe[column], perc_null)

    def _determine_recommendation(self, column_data: pd.Series, percentage_null: float) -> None:
        """Prints to the user some simple recommendations on what to do based on data type and what % of rows are null.

        Args:
            column_data (pd.Series): A pandas series containing a column's values.
            percentage_null (float): The percentage of values that are null (in decimal form).
        """
        # TODO: Provide recommendation to handle date types.
        
        high_perc_flag: bool = percentage_null > 0.3
        dtype_as_string: str = str(column_data.dtype)[0]

        if dtype_as_string == 'o':
            most_common_value: str = column_data.value_counts().index[0]
            self._show_recommendation(column_type=dtype_as_string, high_perc_flag=high_perc_flag)
            print(f"\tMost common value: {most_common_value}")
        elif dtype_as_string in ['i', 'f', 'u', 'c']:
            mean_value: int|float = column_data.mean()
            median_value: int|float = column_data.median()
            mode_value: int|float = column_data.mode().index[0]
            self._show_recommendation(column_type=dtype_as_string, high_perc_flag=high_perc_flag)
            print(f"\tMean: {mean_value}, median: {median_value}, mode: {mode_value}")
        else:
            print(f"--> No recommendations for: {column_data.dtype}.")

    def _show_recommendation(self, column_type: str, high_perc_flag: bool) -> None:
        """Provides the simple logic on what to show user for recommendations.

        Args:
            column_type (str): Must be of type "o", "i", "f", "u", or "c"
            high_perc_flag (bool): A flag used if the percentage is 30 or greater.
        """

        validate_argument(valid_arg_options=["o", "i", "f", "u", "c"], user_input=column_type, parameter_name="column_type")

        if column_type == 'o':
            if high_perc_flag:
                    print("--> String value and high percentage of nulls, possibly ignore.")
            else:
                print("--> String value and low percentage of nulls, possibly fill na values with most common value or as 'Unknown'.")
        else:
            if high_perc_flag:
                print("--> Numeric value and high percentage of nulls, possibly ignore.")
            else:
                print("--> Numeric value and low percentage of nulls, possibly fill with mean, median, mode, or forward fill.")
            
    def __str__(self) -> str:
        return f"This is a pandas DataFrame object. Here are the first 25 rows: {self._dataframe.head(25)}"

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
    
