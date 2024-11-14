# ElPsychicMustache
# 2024-11-13 - created

# This class is used to perform the visualization of feature understanding step.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class FeatureAnalyzer:
    def __init__(self, dataframe) -> None:
        self._dataframe: pd.DataFrame = dataframe
        self.understand_features()

    def understand_features(self):
        self._get_column_dtypes()

    def _get_column_dtypes(self):
        ...