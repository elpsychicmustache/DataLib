# ElPsychicMustache
# 2024-11-13 - created

# This class is used to perform the visualization of feature understanding step.

import pandas as pd
import math
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
        sub_plot_columns:int = 3

        if self._column_dtypes["numeric"]:
            print("Creating histograms . . .")
            numeric_columns: list[str] = self._column_dtypes["numeric"]

            data: pd.DataFrame = self._dataframe[numeric_columns].melt(value_name="value", var_name="variable")

            g = sns.FacetGrid(
                data=data,
                col="variable",
                col_wrap=sub_plot_columns,
                sharex=False,
                sharey=False
            )
            g.map_dataframe(sns.histplot, x="value", bins=20)
            axes = g.axes

            for ax in axes:
                ax.set_ylabel("count", loc="top")
            
        if self._column_dtypes["string"]:
            object_columns: list[str] = self._column_dtypes["string"]

            data = (
                self._dataframe[object_columns]
                .melt().groupby("variable")["value"].value_counts().reset_index()
                .groupby("variable").apply(lambda x: x.nlargest(20, 'count'), include_groups=False).reset_index()
            )
            data["value"] = data["value"].apply(lambda x: f"{x[:30]}..." if len(x) > 30 else f"{x}")

            g = sns.FacetGrid(
                    data=data,
                    col="variable",
                    col_wrap=1,
                    sharex=False,
                    sharey=False
                )
            g.map_dataframe(sns.barplot, x="count", y="value", orient="h", estimator="mean")

            axes = g.axes

            for ax in axes:
                ax.set_ylabel("")

        plt.show()

    def _create_hist_plot(self, series_to_plot: pd.Series) -> plt.matplotlib.axes.Axes:
        # TODO: calculate a way to find the best bins
        # ax = series_to_plot.plot.hist()
        # ax = self._format_plot(ax=ax, plot_type="hist", column_name=series_to_plot.name)
        # return ax
        pass

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

    