# ElPsychicMustache
# 2024-11-24

# Moving the column renaming and column removing, as well as dtype changing methods to it's own class.

import pandas as pd

class ColumnHandler:
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

