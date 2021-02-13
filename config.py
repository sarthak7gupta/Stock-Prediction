from os import getenv

from pytz import timezone


class Config:
    STOCKS = {
        "Indices": ({"NIFTY Bank": "BANKNIFTY"}, True),
        "Stocks": (
            {
                "Axis Bank": "AXISBANK",
                "Bandhan Bank": "BANDHANBNK",
                "Bank of Baroda": "BANKBARODA",
                "Federal Bank": "FEDERALBNK",
                "HDFC Bank": "HDFCBANK",
                "ICICI Bank": "ICICIBANK",
                "IDFC First Bank": "IDFCFIRSTB",
                "IndusInd Bank": "INDUSINDBK",
                "Kotak Mahindra Bank": "KOTAKBANK",
                "Punjab National Bank": "PNB",
                "RBL Bank": "RBLBANK",
                "State Bank of India": "SBIN",
            },
            False,
        ),
    }
    SQLALCHEMY = {
        "drivername": "mysql+pymysql",
        "username": "root",
        "password": getenv("MYSQL_PASSWORD"),
        "host": "127.0.0.1",
        "port": 3306,
        "database": "capstone",
    }
    BASEDIR = "data"
    PATHS = {
        "csv": {"Indices": f"{BASEDIR}/csv/indices", "Stocks": f"{BASEDIR}/csv/stocks"}
    }
    NSECOLUMNS = {
        "Indices": ("Open", "High", "Low", "Close", "Volume", "Turnover"),
        "Stocks": ("Symbol", "Series", "Prev Close", "Open", "High", "Low", "Last", "Close", "VWAP", "Volume", "Turnover", "Trades", "Deliverable_Volume", "Percent_Deliverble")
    }
    TIMEZONE = timezone("Asia/Kolkata")
    LOGS = {
        "default": {
            "filename": "root.log",
            "level": "INFO"
        },
        "fetch": {
            "filename": "fetch.log",
            "level": "INFO"
        },
        "cron": {
            "filename": "cron.log",
            "level": "INFO"
        },
        "debug": {
            "filename": "debug.log",
            "level": "DEBUG"
        },
    }
    CRONJOBS = {
        "data_fetch": {
            "module": "data_service",
            "function": "run_service",
            "trigger": "cron",
            "job_kwargs": {
                "hour": 17,
                "minute": 30
            }
        }
    }
    CRONPIDFILE = "/tmp/cron_pid"
