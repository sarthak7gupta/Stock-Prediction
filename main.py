# %%
import math
# from random import choice

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, Series
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

from arima import ARIMA
from helper import (LogScaler, MinMaxScaler, StockHelper,
                    get_next_n_trading_days, save_predictions)
from lstm import LSTM
from svm import SVM
from hmm import HMM

# %%
stocks = StockHelper.get_stock_symbol_mapping()
# stock, symbol = choice(list(stocks.items()))
stock, symbol = "State Bank", "SBIN"

# %%
total_days = 300
train_size = 0.9
testing = train_size != 1

# %%
# model_name = "SVM"
model_name = "HMM"
# mode_name = "ARIMA"
# model_name = "LSTM"

if model_name == "ARIMA":
    model = ARIMA(symbol, total_days, train_size, scaler=LogScaler)

elif model_name == "LSTM":
    model = LSTM(symbol, total_days, train_size, scaler=MinMaxScaler, is_keras=True)

elif model_name == "SVM":
    model = SVM(symbol, total_days, train_size, scaler=StandardScaler)

elif model_name == "HMM":
    model = HMM(symbol, total_days, train_size, save_model=False)

else:
    exit(0)

# %%
# if model.model: continue

train_data = model.train_data

if testing:
    n_days = 0
    test_data = model.test_data

else:
    n_days = 10
    test_data = Series(index=get_next_n_trading_days(n_days))

# %%
fig, ax = plt.subplots(figsize=(10, 6))
ax.grid(True)
ax.set_title(stock)
ax.set_xlabel("Dates")
ax.set_ylabel("Closing Price")
ax.plot(train_data, c="red", label="Training Data")
ax.plot(test_data, c="black", label="Testing Data")
ax.legend()
plt.show()

# %%
predictions = model.fit_predict(n_days)
predictions
# %%
predictions = Series(data=predictions, index=test_data.index[:len(predictions)])

# %%
save_predictions(
    predictions, type(model).__name__, symbol, train_data.index.max().to_pydatetime()
)

# %%
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(train_data, c="red", label="Training Data")
ax.plot(test_data, c="black", label="Testing Data")
ax.plot(predictions, c="green", label="Predicted Price")
ax.grid(True)
ax.legend()
plt.show()

# %%
if testing:
    mae_score = mean_absolute_error(test_data, predictions)
    print(f"MAE: {mae_score}")
    rmse_score = math.sqrt(mean_squared_error(test_data, predictions))
    print(f"RMSE: {rmse_score}")
    normalised_rmse_score = mean_squared_error(test_data, predictions, squared=False) / (
        test_data.max() - test_data.min()
    )
    print(f"NRMSE: {normalised_rmse_score}")
    mape_score = np.mean(np.abs(predictions - test_data) / np.abs(test_data))
    print(f"MAPE: {mape_score}")

# %%
dff = DataFrame({"actual": test_data, "predictions": predictions})
print(dff)

# %%
