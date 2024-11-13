# ElPsychicMustache
# 2024-11-12

# Decided to move the entire NullAnalysis step of DataframeManager.process_data step, since it is a hefty process.
#   The idea is to abstract that step a little more and make DataframeManager more clean

import pandas as pd

from .utilities import prompt_selection_for_column_list, prompt_user_for_int 
from .validate_input import get_user_confirmation, validate_argument

class NullAnalyzer:
    def __init__(self, dataframe: pd.DataFrame):
        """Takes in a dataframe as an argument, and then performs all null analysis steps.
        You will want to 

        Args:
            dataframe (pd.DataFrame): The dataframe to analyze.
        """
        self._dataframe = dataframe
        self.analyze_nulls()

    def analyze_nulls(self) -> None:
            
        if get_user_confirmation(message="[*] Would you like to analyze null values? [Y/n] ", true_options=["yes", "y", ""], false_options=["no", "n"]):
            self._show_null_values()
            columns_with_null: list[str] = self._get_columns_with_null()
            print()  # making output a bit nicer
            self._display_null_ratios(columns_with_null=columns_with_null)
            print()
            self._prompt_handle_nulls(columns_with_null=columns_with_null)

    def _show_null_values(self):
        """Prints how many null values appear in each column.
        """
        print("======= Null values in each column ======= \n")
        print(f"{self._dataframe.isna().sum()}")

    def _get_columns_with_null(self) -> list[str]:
        """Provides a list of columns that contain null values.

        Returns:
            list[str]: List of columns that contain null values.
        """
        columns_with_nulls_series: pd.Series = self._dataframe.isnull().sum()
        return list(columns_with_nulls_series.loc[columns_with_nulls_series != 0].index)
    
    def _display_null_ratios(self, columns_with_null: list[str]) -> None:
        """Prints out each column, shows the % of rows that are null, and then provides a recommendation on what to do with the null values.

        Args:
            null_columns (list[str]): The list of columns that contain null values.
        """
        if not columns_with_null:
            return

        input("[!] Press enter to continue . . . \n")
        
        num_rows: int = self._dataframe.shape[0]

        print("======= Percentage of null values in each column =======")
        for column in columns_with_null:
            null_percentage: float = self._dataframe[column].isnull().sum() / num_rows
            self._print_column_null_summary(column_name=column, null_percentage=null_percentage)
            self._determine_recommendation(self._dataframe[column], null_percentage)

    def _print_column_null_summary(self, column_name: str, null_percentage: float) -> None:
        print(f"[!] {column_name} {'{:.2%}'.format(null_percentage)}", end="")

    def _determine_recommendation(self, column_data: pd.Series, percentage_null: float) -> None:
        """Prints to the user some simple recommendations on what to do based on data type and what % of rows are null.

        Args:
            column_data (pd.Series): A pandas series containing a column's values.
            percentage_null (float): The percentage of values that are null (in decimal form).
        """

        dtype_as_string: str = str(column_data.dtype)[0]
        high_perc_flag: bool = percentage_null > 0.3

        recommendation_func: dict[str, callable] = {
            'o': self._recommend_for_object_column,
            'i': self._recommend_for_numeric_column,
            'f': self._recommend_for_numeric_column,
            'u': self._recommend_for_numeric_column,
            'c': self._recommend_for_numeric_column,
        }.get(dtype_as_string, self._no_recommendation)

        # using dictionary to call appropriate function
        recommendation_func(dtype_as_string, column_data, high_perc_flag)

    def _recommend_for_numeric_column(self, column_dtype: str, column_data: pd.Series, high_perc_flag: bool) -> None:
        mean_value: int|float = column_data.mean()
        median_value: int|float = column_data.median()
        mode_value: int|float = column_data.mode()[0]
        self._show_recommendation(column_type=column_dtype, high_perc_flag=high_perc_flag)
        print(f"\tMean: {mean_value}, median: {median_value}, mode: {mode_value}")

    def _recommend_for_object_column(self, column_dtype: str, column_data: pd.Series, high_perc_flag: bool) -> None:
        most_common_value: str = column_data.value_counts().index[0]
        self._show_recommendation(column_type=column_dtype, high_perc_flag=high_perc_flag)
        print(f"\tMost common value: {most_common_value}")

    def _no_recommendation(self, column_dtype: str, column_data: pd.Series, high_perc_flag: bool) -> None:
        print(f"--> No recommendations for: {column_dtype}.")

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
            
    def _prompt_handle_nulls(self, columns_with_null: list[str]):
        """Asks if the user wants to do anything to any of the null columns.

        Args:
            columns_with_null (list[str]): The list of columns that contain null values.
        """

        if not columns_with_null:
            return

        print()  # for cleaner output
        
        columns_to_change = prompt_selection_for_column_list(message="[*] Please enter the numbers next to the columns you want to handle null values for. Leaving blank skips this step.", list_of_options=columns_with_null, default_all=False)
        
        if columns_to_change:
            self._ask_how_to_handle_null(list_of_columns=columns_to_change)
    
    def _ask_how_to_handle_null(self, list_of_columns: list[str]) -> None:
        """Handler for how user wants to handle each column.

        Args:
            list_of_columns (list[str]): The list of columns to change.
        """

        options: dict[int, str] = {
            0: "Do nothing",
            1: "Replace with mean",
            2: "Replace with median",
            3: "Replace with mode (or most common value)",
            4: "Forward fill", 
            5: "Remove entire column",
            6: "Remove all rows that contain null values: "
        }
        
        for column in list_of_columns:

            print()  # printing for nicer output
            user_selection: int = prompt_user_for_int(message=f"[*] What would you like to do with column {column}?", options=options)
            
            if user_selection == 0:
                print("[!] Doing nothing.")
                pass
            elif user_selection == 1:
                self._replace_with_mean_median_mode(column=column, method="mean")
            elif user_selection == 2:
                self._replace_with_mean_median_mode(column=column, method="median")
            elif user_selection == 3:
                self._replace_with_mean_median_mode(column=column, method="mode")
            elif user_selection == 4:
                self._replace_with_ffill()
            elif user_selection == 5:
                self._drop_nulls(column=column, axis=1)
            elif user_selection == 6:
                self._drop_nulls(column=column, axis=0)
                
    # Null replacement suite
    def _replace_with_mean_median_mode(self, column: str, method: str) -> None:
        if method == "mean":
            mean: float|int = self._dataframe[column].mean()
            print(f"[!] Replacing null values with the mean {mean}")
            self._dataframe[column] = self._dataframe[column].fillna(mean)
        elif method == "median":
            median: float|int = self._dataframe[column].median()
            print(f"[!] Replacing null values with the median {median}")
            self._dataframe[column] = self._dataframe[column].fillna(median)
        elif method == "mode":
            mode: float|int|str = self._dataframe[column].mode()[0]
            print(f"[!] Replacing null values with the mode {mode}")
            self._dataframe[column] = self._dataframe[column].fillna(mode)

    def _replace_with_ffill(self, column: str) -> None:
        print("[!] Replacing null values with forward filling.")
        self._dataframe[column] = self._dataframe[column].fillna(method="ffill")

    def _drop_nulls(self, column: str, axis: int) -> None:
        if axis == 0:
            print(f"[!] Removing all rows that contain null values in {column}")
            self._dataframe = self._dataframe.dropna(subset=[column])
        elif axis == 1:
            print(f"[!] Removing column {column}")
            self._dataframe = self._dataframe.drop(columns=[column])
    # End null replacement suite

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe
