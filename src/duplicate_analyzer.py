# ElPsychicMustache
# 2024-11-12

import pandas as pd

from .utilities import prompt_selection_for_column_list
from .validate_input import get_user_confirmation

class DuplicateAnalyzer:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe
        self.analyze_duplicates()

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
            self._show_duplicate_example(duplicate_examples=duplicate_rows, subset_list=subset_for_dup_identification)
        
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

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe

