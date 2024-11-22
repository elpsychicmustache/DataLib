# ElPsychicMustache
# 2024-11-13 - created

# This class is used to perform the visualization of feature understanding step.

import matplotlib.pyplot as plt
import pandas as pd
from .validate_input import get_user_confirmation

class FeatureAnalyzer:
    def __init__(self, dataframe) -> None:
        self._dataframe: pd.DataFrame = dataframe
        self._column_dtypes: dict[str, list[str]] = {
            "numeric": [],
            "datetime": [],
            "string": [],
            "bool": [],
            "unknown": []
        }
        self.understand_features()

    def understand_features(self) -> None:
        self._get_column_dtypes()
        self._call_plots_from_dtypes()

    def _get_column_dtypes(self) -> None:
        """Populates the private variable _column_dtypes with a masked version of each column's dtype.
        """
        
        for column in self._dataframe.columns:
            column_dtype: str = self._dataframe[column].dtype
            if pd.api.types.is_numeric_dtype(column_dtype):
                self._column_dtypes["numeric"].append(column)
            elif pd.api.types.is_datetime64_dtype(column_dtype):
                self._column_dtypes["datetime"].append(column)
            elif pd.api.types.is_string_dtype(column_dtype):
                self._column_dtypes["string"].append(column)
            elif isinstance(self._dataframe[column].dtypes, pd.CategoricalDtype):
                self._column_dtypes["string"].append(column)  # saving categorical data as string
            elif pd.api.types.is_bool_dtype(column_dtype):
                self._column_dtypes["bool"].append(column)
            else:
                self._column_dtypes["unknown"].append(column)

    def _call_plots_from_dtypes(self):
        """Takes the columns for each dtype, and then sends to the appropriate plotting method to show distribution.
        """

        self._call_numeric_plots()
        self._call_object_plots()

    def _call_numeric_plots(self):
        numeric_columns: list[str] = self._column_dtypes["numeric"]

        if not get_user_confirmation(message=f"[*] Would you like to display the {len(numeric_columns)} numeric graphs? (Y/n): ", true_options=["y","yes", ""], false_options=["n", "no"]):
            return
        
        figures: list = []

        for index, column in enumerate(numeric_columns):
            if index == 0:
                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(numeric_columns)}")
                self._create_hist_plot(self._dataframe[column])
            elif (index % 5 == 0):
                plt.show()
                figures = []  # restting figures

                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(numeric_columns)}")
                self._create_hist_plot(self._dataframe[column])
            else:
                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(numeric_columns)}")
                self._create_hist_plot(self._dataframe[column])
        
        if figures:
            plt.show()

    def _call_object_plots(self):
        string_columns: list[str] = self._column_dtypes["string"]
        if not get_user_confirmation(message=f"[*] Would you like to display the {len(string_columns)} numeric graphs? (Y/n): ", true_options=["y","yes", ""], false_options=["n", "no"]):
            return

        figures: list = []

        for index, column in enumerate(string_columns):
            if index == 0:
                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(string_columns)}")
                self._create_bar_plot(self._dataframe[column])
            elif (index % 5 == 0):
                plt.show()
                figures = []  # restting figures

                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(string_columns)}")
                self._create_bar_plot(self._dataframe[column])
            else:
                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(string_columns)}")
                self._create_bar_plot(self._dataframe[column])
        
        if figures:
            plt.show()

    def _create_hist_plot(self, series_to_plot: pd.Series) -> plt.matplotlib.axes.Axes:
        ax = series_to_plot.plot.hist()
        ax.set_title(f"{series_to_plot.name} histogram", loc="left")
        ax.set_ylabel("frequency", loc="top")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        return ax

    def _create_bar_plot(self, series_to_plot: pd.Series) -> plt.matplotlib.axes.Axes:
        top_20_values: pd.Series = series_to_plot.value_counts().head(20)

        for index in top_20_values.index:
            if len(index) > 30:
                top_20_values = top_20_values.rename(index={index: f"{index[:27]}..."})

        ax = top_20_values.plot.barh()
        ax.set_title(f"{series_to_plot.name} top {len(top_20_values)} values", loc="left")  # using len(top_20_values) in case there are less than 20 values
        ax.set_xlabel("frequency", loc="left")
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        return ax


    