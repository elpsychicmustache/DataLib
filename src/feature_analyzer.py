# ElPsychicMustache
# 2024-11-13 - created

# This class is used to perform the visualization of feature understanding step.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        if self._column_dtypes["numeric"]:
            numeric_columns: list[str] = self._column_dtypes["numeric"]

            for column in numeric_columns:
                self._create_hist_plot(series_to_plot=self._dataframe[column])

    def _create_hist_plot(self, series_to_plot: pd.Series):
        # TODO: calculate a way to find the best bins
        ax = series_to_plot.plot.hist()
        self._format_plot(ax=ax, plot_type="hist", column_name=series_to_plot.name)

    def _format_plot(self, ax: plt.matplotlib.axes.Axes, plot_type: str, column_name:str):
        ax.spines[["right", "top"]].set_visible(False)
        if plot_type == "bar":
            ax.set_title(f"{column_name} top 20 values", loc="left")
        elif plot_type == "hist":
            ax.set_title(f"{column_name} histogram", loc="left")
        ax.set_ylabel("frequency", loc="top")
        plt.show()

    