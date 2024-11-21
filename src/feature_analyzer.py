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

        print(f"TROUBLESHOOTING _column_dtypes: {self._column_dtypes}")  # FOR TROUBLESHOOTING - REMOVE LATER

    def _call_plots_from_dtypes(self):
        """Takes the columns for each dtype, and then sends to the appropriate plotting method to show distribution.
        """

        self._call_numeric_plots()

    def _call_numeric_plots(self):
        if not get_user_confirmation(message=f"[*] Would you like to display the {len(self._column_dtypes["numeric"])} numeric graphs? (Y/n): ", true_options=["y","yes", ""], false_options=["n", "no"]):
            return
        
        numeric_columns: list[str] = self._column_dtypes["numeric"]

        figures: list = []

        for index, column in enumerate(numeric_columns):
            if index == 0:
                figures.append(plt.figure())
                print(f"[!] Creating plot {index + 1}/{len(numeric_columns)}")
                self._create_hist_plot(self._dataframe[column])
            elif (index % 5 == 0):
                plt.show()
                input = "Press enter to continue . . . "
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

    def _create_hist_plot(self, series_to_plot: pd.Series) -> plt.matplotlib.axes.Axes:
        # TODO: calculate a way to find the best bins
        # ax = series_to_plot.plot.hist()
        # ax = self._format_plot(ax=ax, plot_type="hist", column_name=series_to_plot.name)
        # return ax
        ax = series_to_plot.plot.hist()
        ax.set_title(f"{series_to_plot.name} histogram", loc="left")
        ax.set_ylabel("frequency", loc="top")
        ax.spines[["top", "right"]].set_visible(False)
        return ax

    def _create_bar_plot(self, series_to_plot: pd.Series) -> plt.matplotlib.axes.Axes:
        ax = series_to_plot.value_counts().head(20).plot.bar()
        ax = self._format_plot(ax=ax, plot_type="bar", column_name=series_to_plot.name)
        return ax

    def _format_plot(self, ax: plt.matplotlib.axes.Axes, plot_type: str, column_name:str)  -> plt.matplotlib.axes.Axes:
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_title(column_name, loc="left")
        # if plot_type == "bar":
        #     ax.set_title(f"{column_name} top 20 values", loc="left")
        # elif plot_type == "hist":
        #     ax.set_title(f"{column_name} histogram", loc="left")
        ax.set_ylabel("frequency", loc="top")
        return ax

    