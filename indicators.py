import pandas as pd
import uuid
from ingestion import merge_stock_data


def weighted_moving_average(df: pd.DataFrame, ohlc_column: str = "Close", window_size: int = 20) -> pd.DataFrame:
    """
    weighted_moving_average computes the weighted moving average over the specified column.

    Parameters
    ----------
    df : pd.DataFrame
        The OHLC data.
    ohlc_column : str, optional
        The OHLC column, e.g., "Close", by default "Close"
    window_size : int, optional
        The window size, by default 20

    Returns
    -------
    pd.DataFrame
        The OHLC data, with columns "{ohlc_column}_weighted_moving_average" and "{ohlc_column}_weighted_moving_std_dev"
    """
    df[f'{ohlc_column}_weighted_moving_average'] = df[ohlc_column].rolling(window=window_size).mean()
    df[f'{ohlc_column}_weighted_moving_std_dev'] = df[ohlc_column].rolling(window=window_size).std()
    return df


def bollinger_bands(df: pd.DataFrame, ohlc_column: str = "Close") -> pd.DataFrame:
    """
    bollinger_bands computes the bollinger bands over the specified column.

    Parameters
    ----------
    df : pd.DataFrame
        The OHLC data, assumes to have columns "{ohlc_column}_weighted_moving_average" and "{ohlc_column}_weighted_moving_std_dev"
    ohlc_column : str, optional
        The OHLC column, e.g., "Close", by default "Close"

    Returns
    -------
    pd.DataFrame
        The OHLC data, with columns "{ohlc_column}_upper_band" and "{ohlc_column}_lower_band"
    """
    df[f'{ohlc_column}_upper_band'] = df[f'{ohlc_column}_weighted_moving_average'] + (df[f'{ohlc_column}_weighted_moving_std_dev'] * 2)
    df[f'{ohlc_column}_lower_band'] = df[f'{ohlc_column}_weighted_moving_average'] - (df[f'{ohlc_column}_weighted_moving_std_dev'] * 2)
    return df


def rsi(df: pd.DataFrame, ohlc_column: str = "Close", window_size: int = 14) -> pd.DataFrame:
    """
    rsi computes the RSI over the specified column.

    Parameters
    ----------
    df : pd.DataFrame
        The OHLC data
    ohlc_column : str, optional
        The OHLC column, e.g., "Close", by default "Close"
    window_size : int, optional
        Period for RSI calculation, by default 14

    Returns
    -------
    pd.DataFrame
        _description_
    """
    uid = uuid.uuid4()
    # Calculate daily price changes
    df[f'{ohlc_column}_Price Change_{uid}'] = df[ohlc_column].diff()
    # # Calculate gains and losses
    df[f'{ohlc_column}_Gain_{uid}'] = df[f'{ohlc_column}_Price Change_{uid}'].apply(lambda x: x if x > 0 else 0)
    df[f'{ohlc_column}_Loss_{uid}'] = df[f'{ohlc_column}_Price Change_{uid}'].apply(lambda x: -x if x < 0 else 0)
    # Calculate the average gain and average loss
    df[f'{ohlc_column}_Avg Gain_{uid}'] = df[f'{ohlc_column}_Gain_{uid}'].rolling(window=window_size, min_periods=1).mean()
    df[f'{ohlc_column}_Avg Loss_{uid}'] = df[f'{ohlc_column}_Loss_{uid}'].rolling(window=window_size, min_periods=1).mean()
    # Calculate RS and RSI
    df[f'{ohlc_column}_RS_{uid}'] = df[f'{ohlc_column}_Avg Gain_{uid}'] / df[f'{ohlc_column}_Avg Loss_{uid}']
    df[f'{ohlc_column}_RSI'] = 100 - (100 / (1 + df[f'{ohlc_column}_RS_{uid}']))
    # Drop columns we dont need
    df.drop([
        f'{ohlc_column}_Price Change_{uid}',
        f'{ohlc_column}_Gain_{uid}',
        f'{ohlc_column}_Loss_{uid}',
        f'{ohlc_column}_Avg Gain_{uid}',
        f'{ohlc_column}_Avg Loss_{uid}',
        f'{ohlc_column}_RS_{uid}'],
            axis=1,
            inplace=True
    )
    return df


if __name__ == '__main__':
    files_dict = {
        "": r"data\GBPJPY_Candlestick_1_D_BID_01.01.2014-03.08.2024.csv",
        "barclays_": r"data\barclays_stock.csv",
        "mitsui_": r"data\mitsui_stock.csv",
        # "hitachi_": r"data\hitachi_stock.csv",
        "nissan_": r"data\nissan_stock.csv",
        "honda_": r"data\honda_stock.csv",
        "sony_": r"data\sony_stock.csv"
    }

    df = merge_stock_data(files_dict)

    print(df.tail(20))
    df['Close'] = df['Close'].shift(-1)  # shifting to treat Closing price as label
    # NOTE: Multi-Label / Multi-Output forecasting

    # df['Gmt time'] = pd.to_datetime(df['Gmt time'], dayfirst=True)

    # df['Gmt time'] = df['Gmt time'].dt.date

    # df.set_index('Gmt time')

    # Calculate the moving average, standard deviation, and Bollinger Bands
    df = weighted_moving_average(df=df, ohlc_column="Close", window_size=20)
    df = bollinger_bands(df=df, ohlc_column="Close")
    df = rsi(df=df, ohlc_column="Close", window_size=14)

    print(df.tail(20))
