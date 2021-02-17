import threading
from datetime import date
from functools import wraps
from os import path
from time import sleep, time

import pandas as pd
from nsepy import get_history
from pandas.errors import EmptyDataError
from tqdm import tqdm

from config import Config
from database.SQLModel import StockPrice
# from database.NoSQLModel import StockPrice
from db_helper import session_scope
from log_helper import logging

logger = logging.getLogger("default")
anim = r"|/-\|"
columns = Config.NSECOLUMNS


class ElapsedTimeThread(threading.Thread):
    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time()

        while not self.stopped():
            print(f"...{time() - thread_start:.2f} seconds elapsed", end="\r")
            sleep(0.25)

        print(f"Took {time() - thread_start:.2f} seconds\033[K")


def elapsed_time_update(f):
    @wraps(f)
    def print_elapsed_time(*args, **kwargs):
        (thread := ElapsedTimeThread()).start()
        return_val = None

        try:
            return_val = f(*args, **kwargs)

        except KeyboardInterrupt:
            thread.stop()
            thread.join()

        thread.stop()
        thread.join()

        return return_val

    return print_elapsed_time


@elapsed_time_update
def fetch_and_store_csv(
    symbol: str,
    data_dir: str,
    is_index: bool,
    set_key: str,
    from_date: date,
    to_date: date = date.today(),
) -> pd.DataFrame:
    hist = pd.DataFrame()

    try:
        hist = get_history(symbol=symbol, start=from_date, end=to_date, index=is_index)
        concat_df_to_csv(hist, f"{data_dir}/{symbol}.csv")

        if hist.empty:
            raise EmptyDataError

        hist.columns = columns[set_key]
        hist = hist[~hist.index.duplicated()]
        hist = hist.where(pd.notnull(hist), 0)
        hist = hist.round(3)
        hist = hist.astype({"Volume": int})
        if not is_index: hist = hist.astype({"Trades": int, "Deliverable_Volume": int})
        hist.replace({0: None})

    except EmptyDataError:
        logger.warning(f"No data fetched for {symbol} from NSE")

    except Exception as e:
        logger.error(f"Error {e} while fetching {symbol} from NSE")

    else:
        logger.info(f"Fetched {symbol}")

    finally:
        return hist


def store_db(df: pd.DataFrame, stock_id: int, name: str):
    for (idx, row) in tqdm(
        df.iterrows(), desc=f"Storing {name} to db", unit=" rows", total=len(df)
    ):
        stock_price = StockPrice(
            date=idx,
            stock_id=stock_id,
            open_price=row.Open or None,
            high_price=row.High or None,
            low_price=row.Low or None,
            close_price=row.Close or None,
            volume=row.Volume or None,
            vwa_price=row.get("VWAP"),
            trades=row.get("Trades"),
            deliverable_volume=row.get("Deliverable_Volume"),
        )

        try:
            with session_scope(autocommit=True) as session:
                session.add(stock_price)
                session.flush()

        except Exception as e:
            logger.error(f"Error {e} while adding StockPrice for {name}. Rows {stock_price}")


def concat_df_to_csv(df: pd.DataFrame, csv_path: str):
    df_csv = (
        pd.read_csv(csv_path, index_col=0, parse_dates=[0])
        if path.exists(csv_path)
        else pd.DataFrame()
    )
    df_csv.combine_first(df).to_csv(csv_path)


def display_time(sec: int):
    print(f"\rCooldown: {anim[sec % len(anim)]} 00:{sec:02} remaining", end="", flush=True)


def countdown(sec: int):
    print("-" * 27)
    display_time(sec)

    while (sec := sec - 1) >= 0:
        sleep(1)
        display_time(sec)

    print()
    print("-" * 27)
