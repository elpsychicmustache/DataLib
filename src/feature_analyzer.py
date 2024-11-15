# ElPsychicMustache
# 2024-11-13 - created

# This class is used to perform the visualization of feature understanding step.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class FeatureAnalyzer:
    def __init__(self, dataframe) -> None:
        self._dataframe: pd.DataFrame = dataframe
        self._column_dtypes: dict[str, str] = {}
        self.understand_features()

    def understand_features(self):
        self._get_column_dtypes()

    def _get_column_dtypes(self):
        
        for column in self._dataframe.columns:
            column_dtype: str = self._dataframe[column].dtype
            if pd.api.types.is_numeric_dtype(column_dtype):
                self._column_dtypes[column] = "numeric"
            elif pd.api.types.is_datetime64_dtype(column_dtype):
                self._column_dtypes[column] = "datetime"
            elif pd.api.types.is_string_dtype(column_dtype):
                self._column_dtypes[column] = "string"
            elif isinstance(self._dataframe[column].dtypes, pd.CategoricalDtype):
                self._column_dtypes[column] = "string"  # saving categorical data as string
            elif pd.api.types.is_bool_dtype(column_dtype):
                self._column_dtypes[column] = "bool"
            else:
                self._column_dtypes[column] = "unknown"

        print(self._column_dtypes)