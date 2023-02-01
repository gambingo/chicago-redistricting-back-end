import pandas as pd

from directories import DATA_DIR


def load_cleaned_data():
    df = pd.read_pickle(DATA_DIR / "tract_populations.pkl")
    return df


def load_clean_and_save_raw_data():
    filename = "2020-census/DECENNIALPL2020.P2_2023-01-17T154516/DECENNIALPL2020.P2-Data.csv"
    df = pd.read_csv(DATA_DIR / filename, header=1)
    df = clean_data(df)
    df = df.groupby("Census Tract").sum(numeric_only=True) \
        .drop(columns=['Block', 'Block Group'])
    df.to_pickle(DATA_DIR / "tract_populations.pkl")
    return df


def clean_data(df):
    # Drop columns that are all NaN
    df = df.dropna(axis=1, how="all")

    # These column labels are mad gross
    df = clean_column_names(df)
    
    mvp_columns = [
        "Geography",
        "Geographic Area Name",
        "Total",
    ]
    df = df[mvp_columns].copy()
    df.rename(columns={"Total": "Population"}, inplace=True)

    df = parse_geographic_area_name(df)
    return df


def clean_column_names(df):
    df = df.rename(columns={" !!Total:": "Total"})
    renames = {col: col.replace(" !!Total:!!","").replace("!!"," ") for col in df.columns}
    df = df.rename(columns=renames)
    return df


def parse_geographic_area_name(df):
    """
    Example: 'Block 4010, Block Group 4, Census Tract 8157.02, Cook County, Illinois'
    """
    full_column = "Geographic Area Name"
    func = lambda area_name: [x.strip() for x in area_name.split(",")]
    columns = ["Block", "Block Group", "Census Tract", "County", "State"]
    df[columns] = df[full_column].apply(
        lambda row: pd.Series(func(row)))

    for col in ["Block", "Block Group", "Census Tract"]:
        df[col] = df[col].apply(lambda string: string.replace(col+" ", ""))
        df[col] = df[col].astype(float)
    
    df.drop(columns=[full_column], inplace=True)
    return df


if __name__ == "__main__":
    _ = load_clean_and_save_raw_data()