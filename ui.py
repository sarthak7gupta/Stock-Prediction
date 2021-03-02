from datetime import datetime

from arima import ARIMA
from database.SQLModel import Stock, StockPrediction, StockPrice
from db_helper import session_scope
from helper import StockHelper
from lstm import LSTM
from svm import SVM
from hmm import HMM

ch = input("Interactive = 1: ")

stocks = StockHelper.list_all_symbols()

for i, s in enumerate(stocks, 1):
    print(f"({i}) {s}")

print("Select Stock: ")
i = int(input()) if ch else 12

symbol = stocks[i - 1]
print(symbol)
print()

models = {"ARIMA": ARIMA, "LSTM": LSTM, "SVM": SVM, "HMM": HMM}

m_k, m_v = zip(*models.items())

for i, s in enumerate(m_k, 1):
    print(f"({i}) {s}")

print("Enter Model: ")
i = int(input()) if ch else 4

m = m_k[i - 1]
model = m_v[i - 1]
print(m)
print()

print("Date (YYYY-MM-DD): ")
d = (
    datetime.strptime(input(), "%Y-%m-%d").date()
    if ch
    else datetime(2021, 3, 1).date()
)
print(d)
print()

with session_scope() as ssn:
    stock = ssn.query(Stock).filter(Stock.symbol == symbol).first()

    if not stock:
        raise Exception("Invalid Stock ID")

    stock_id = stock.id

    pred = (
        ssn.query(StockPrediction)
        .filter(
            StockPrediction.stock_id == stock_id,
            StockPrediction.date == d,
            StockPrediction.predictor_model == m,
        )
        .order_by(StockPrediction.prediction_as_of)
        .first()
    )

    actual = (
        ssn.query(StockPrice).filter(StockPrice.stock_id == stock_id, StockPrice.date == d).first()
    )

    if not pred:
        print("No prediction")

    else:
        a = actual.close_price
        p = pred.predicted_price
        print("Actual:", a)
        print("Predicted:", p)
        print(f"{abs(a - p) / p * 100}% difference")
