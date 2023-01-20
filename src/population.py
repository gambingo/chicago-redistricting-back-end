import pandas as pd

from directories import DATA_DIR


def load_data():
    filename = "2020-census/DECENNIALPL2020.P2_2023-01-17T154516/DECENNIALPL2020.P2-Data.csv"
    df = pd.read_csv(DATA_DIR / filename, header=1)
    df = clean_data(df)
    return df


def clean_data(df):
    # Drop columns that are all NaN
    df = df.dropna(axis=1, how="all")

    # These column labels are mad gross
    df = clean_column_names(df)
    return df


def clean_column_names(df):
    df = df.rename(columns={" !!Total:": "Total"})
    renames = {col: col.replace(" !!Total:!!","").replace("!!"," ") for col in df.columns}
    df = df.rename(columns=renames)
    return df
