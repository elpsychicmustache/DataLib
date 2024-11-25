# ElPsychicMustache
# 2024-11-24

# Moving the column renaming and column removing, as well as dtype changing methods to it's own class.

import pandas as pd

from utilities import prompt_selection_for_column_list
from validate_input import get_user_confirmation

class ColumnHandler:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self._dataframe = dataframe

    def remove_columns(self) -> None:
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

    def rename_columns(self) -> None:
        pass

    def analyze_dtypes(self) -> None:
        pass

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._dataframe