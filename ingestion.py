import pandas as pd


def merge_stock_data(files_dict, index_col: str = 'Gmt time') -> pd.DataFrame:
    """
    merge_stock_data reads the OHLC data from different stock files and merges them horizontally into a single dataframe.

    Parameters
    ----------
    files_dict : dict[str, str]
        A dictionary with column prefixes as keys and file paths as values.
    index_col : str, optional
        The name of the index column in all the files, by default 'Gmt time'.

    Returns
    -------
    pd.DataFrame
        The merged dataframe.
    """
    dfs = {}
    date_format = "%Y-%m-%d"  # Define the desired date format

    # Step 1: Load and clean data
    for prefix, file_path in files_dict.items():
        df = pd.read_csv(file_path, index_col='Gmt time')
        # special case for this data
        if prefix == 'sonia_tona_diff_':
            df=df[['tona_sonia_difference']]

        # Clean and standardize 'Gmt time' column
        df.index = pd.to_datetime(df.index, errors='coerce')  # Convert index to datetime
        df.index = df.index.date  # Extract date part only

        # Ensure uniform date format
        df.index = pd.to_datetime(df.index, format=date_format)
        df = df.add_prefix(f"{prefix}")

        # Save DataFrame to dictionary
        dfs[prefix] = df

    # Step 2: Find the lowest common date
    start_dates = [df.index.min() for df in dfs.values()]
    end_dates = [df.index.max() for df in dfs.values()]

    first_mutual_date = max(start_dates)
    last_mutual_date = min(end_dates)



    # Step 3: Filter DataFrames to include only rows within the mutual date range
    for key in dfs:
        dfs[key] = dfs[key].loc[(dfs[key].index >= first_mutual_date) & (dfs[key].index <= last_mutual_date)]

    # Step 4: Concatenate all DataFrames
    merged_df = pd.concat(dfs.values(), axis=1)



    return merged_df


def extract() -> pd.DataFrame:
    """
    extract all the data from all the different data sources and create a pandas dataframe for later processing.

    Returns
    -------
    pd.DataFrame
        A single pandas dataframe that contains the raw data.
    """
    """
    extract all the data from all the different data sources and create a pandas dataframe for later processing.

    Returns
    -------
    pd.DataFrame
        A single pandas dataframe that contains the raw data.
    """
    files_dict = {
        # GBP TO JPY Data
        "": r"data\GBPJPY_Candlestick_1_D_BID_01.01.2014-03.08.2024.csv",
        # Currencies Corrleation
        "EURJPY_": r"data\EURJPY_Candlestick_1_D_BID_01.01.2014-03.08.2024.csv",
        "AUDJPY_": r"data\AUDJPY_Candlestick_1_D_BID_01.01.2014-03.08.2024.csv",
        "USDJPY_": r"data\USDJPY_Candlestick_1_D_BID_01.01.2014-03.08.2024.csv",
        # Stocks
        "barclays_": r"data\barclays_stock.csv",
        "mitsui_": r"data\mitsui_stock.csv",
        # "hitachi_": r"data\hitachi_stock.csv",
        "nissan_": r"data\nissan_stock.csv",
        "honda_": r"data\honda_stock.csv",
        "sony_": r"data\sony_stock.csv",
        "sonia_tona_diff_": r"data\tona_sona_diff_from_2014_to_2024 (1).csv"
    }

    df = merge_stock_data(files_dict)

    # TODO: Handle time discrepencies between different sources (Vladi).
    # TODO: Add generic time-series data to the model, e.g., holidays, economic calendars, etc.
    return df


if __name__ == '__main__':
    df = extract()
    print(df)
    print(df.info())


