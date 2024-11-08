# ElPsychicMustache
# 2024-11-04

import pandas as pd

# TODO: Move full_file_path to validate_input

def get_df_from_csv(file_path: str, file_name: str, date_columns: list[str], column_names: list[str]) -> pd.DataFrame:
    
    # making sure user did not forget to add '/' at the end of file path
    if file_path[-1] != '/':
        file_path += '/'

    full_file_path: str = f"{file_path}{file_name}"

    read_csv_kwargs: dict = {}

    if date_columns:
        read_csv_kwargs['parse_dates'] = date_columns
    if column_names:
        read_csv_kwargs['names'] = column_names

    return pd.read_csv(full_file_path, **read_csv_kwargs)
