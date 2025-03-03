import os
import argparse
import dateutil.parser
from datetime import datetime, date

from duka.app import app
from duka.core.utils import set_up_signals, valid_timeframe


def valid_date(s: str | datetime | date | None) -> date:
    try:
        return dateutil.parser.parse(str(s), fuzzy=True).date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def scrape_dukascopy_data(
        symbols: str | list[str] = "EURUSD",
        day: str | datetime | date | None = None,
        startdate: str | datetime | None = None,
        enddate: str | datetime | None = None,
        n_threads: int | None = None,
        granularity: str | None = None,
        foldername: str = '.'
    ):
    """
    Scrape data from dukascopy.

    Parameters
    ----------
    symbols : str | list[str]
        symbols to scrape
        Default: "EURUSD"
    day : str | datetime
        for scraping only one day, and it will override startdate and enddate if they are Not specified.
        Default: None, which is inferred as today.
    startdate : str | datetime
        start date of the range of days to scrape
        Default: None, in which case `day` is used.
    enddate : str | datetime
        end date of the range of days to scrape
        Default: None, in which case `day` is used.
    n_threads : int
        number of threads to use for parallel scraping.
        Default: None, in which case the number of threads is inferred from the number of CPU cores.
    granularity : str
        the granularity level at which the data is aggregated, or 'tick' for ticker level data.
        valid values are: 'tick', 's_30', '1m', '2m', '5m', '10m', '15m', '30m', '1h', '4h', '1d' (case insensitive).
        Default: None, in which case 'tick' is used.
    foldername : str
        the folder to save the data to. The folder will be created in the current working directory if it does not exist.
        Default: '.' (current working directory).
    """
    symbols_list: list[str] = [str(symbols)] if isinstance(symbols, str) else symbols
    final_symbols_list = []
    for symbol in symbols_list:
        symbol = symbol.replace(".", "").replace("/", "").upper()
        final_symbols_list.append(symbol)
    symbols_list = final_symbols_list

    if day is None:
        defualt_day: str | date = datetime.now().strftime("%YYYY-%mm-%dd")
    defualt_day: str | date = valid_date(defualt_day if day is None else day)

    if startdate is not None:
        start = valid_date(startdate)
    else:
        start = defualt_day

    if enddate is not None:
        end = valid_date(enddate)
    else:
        end = defualt_day

    if os.path.isdir(foldername) is False:
        os.mkdir(foldername)

    set_up_signals()
    app(
        symbols=symbols_list,
        start=start,
        end=end,
        threads=n_threads if n_threads is not None else os.cpu_count(),
        timeframe=valid_timeframe(granularity),
        folder=foldername,
        header=True
    )


if __name__ == "__main__":
    # scrape_dukascopy_data(
    #     symbols="COCOA.CMD/USD",
    #     day="2024-07-01",
    #     startdate="2024-07-01",
    #     enddate="2024-08-01",
    #     n_threads=1,
    #     granularity="TICK",
    #     foldername="./data"
    # )

    scrape_dukascopy_data(
        symbols="GBPJPY",
        day="2024-07-01",
        startdate="2024-07-01",
        enddate="2024-08-01",
        n_threads=1,
        granularity="TICK",
        foldername="./data"
    )
