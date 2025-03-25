import pandas as pd
import numpy as np
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from ingestion import extract
from indicators import weighted_moving_average, bollinger_bands, rsi


def train_val_test_split(
    df: pd.DataFrame,
    val_cutoff_date: datetime,
    test_cutoff_date: datetime):
    """
    train_val_test_split split the data into train, validation, and test sets.

    Parameters
    ----------
    df : pd.DataFrame
        _description_
    val_cutoff_date : datetime
        _description_
    test_cutoff_date : datetime
        _description_

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        _description_
    """
    train_data = df[df.index < val_cutoff_date]
    val_data = df[(df.index >= val_cutoff_date) & (df.index < test_cutoff_date)]
    test_data = df[df.index >= test_cutoff_date]
    return train_data, val_data, test_data


def split_time_series(df, train_size=0.8, val_size=0.19):
    # Calculate sizes
    total_size = len(df)
    train_end = int(total_size * train_size)
    val_end = train_end + int(total_size * val_size)

    # Split the DataFrame
    train = df.iloc[:train_end]
    validation = df.iloc[train_end:val_end]
    test = df.iloc[val_end:]

    return train, validation, test


def scale_data(train_data, val_data, test_data):
    # TODO: Find a good scaling algorithm for the data. StandardScaler is basic and not justified theoretically.
    X = df.drop('Close', axis=1)
    y = df['Close']
    scaler = StandardScaler()

    # Fit and transform the data
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    transform the raw data and creates the final features for the model (including indicators).

    Parameters
    ----------
    df : pd.DataFrame
        The raw dataframe, as returned by the `extract` function.

    Returns
    -------
    pd.DataFrame
        The dataframe after all the transformations,
        preprocessing and added features that are required to load into the forecasting model.
    """
    # shift to treat Closing price as label
    df['Close'] = df['Close'].shift(-1)

    # Calculate the moving average, standard deviation, and Bollinger Bands
    df = weighted_moving_average(df=df, ohlc_column="Close", window_size=20)
    df = bollinger_bands(df=df, ohlc_column="Close")
    df = rsi(df=df, ohlc_column="Close", window_size=14)
    # TODO: Create generic time-series FEATURES for the model, e.g., extract year, month and day features from the date, process the holidays data, etc.


    return df


if __name__ == '__main__':
    raw_data = extract()
    preprocessed_data = transform(df=raw_data)
    preprocessed_data.reset_index().to_csv('transformed_data.csv',index = False)
