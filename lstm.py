import pandas as pd
import numpy as np
from keras.layers import LSTM as LSTM_Layer
from keras.layers import Dense, Dropout
from keras.models import Sequential
from tensorflow.python.keras.layers.core import Activation

from base_model import BaseModel


class LSTM(BaseModel):
    window = 60

    def train(self) -> None:
        train_values = self.train_data.values.reshape(-1, 1)

        X_train = np.array(
            [train_values[i - self.window:i, 0] for i in range(self.window, len(train_values))]
        )
        y_train = np.array([train_values[i, 0] for i in range(self.window, len(train_values))])

        X_train = np.reshape(X_train, (*X_train.shape, 1))

        self.model = model = Sequential()
        model.add(LSTM_Layer(60, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM_Layer(60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM_Layer(60, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM_Layer(60, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(1))

        model.compile(optimizer="adam", loss="mean_squared_error")

        model.fit(X_train, y_train, batch_size=32, epochs=200)

        # train_values = self.train_data.values

        # X_train = np.array(
        #     [train_values[i - self.window:i] for i in range(self.window, len(train_values))]
        # )
        # y_train = np.array([train_values[i] for i in range(self.window, len(train_values))])

        # X_train = np.reshape(X_train, (*X_train.shape, 1))

        # neurons = 100
        # dropout = 0.2
        # activation = "tanh"
        # loss = "mse"
        # epochs = 20
        # batch_size = 10

        # self.model = model = Sequential()
        # model.add(
        #     LSTM_Layer(
        #         neurons,
        #         return_sequences=True,
        #         input_shape=(X_train.shape[1], 1),
        #         activation=activation,
        #     )
        # )
        # model.add(Dropout(dropout))
        # model.add(LSTM_Layer(neurons, return_sequences=True, activation=activation))
        # model.add(Dropout(dropout))
        # model.add(LSTM_Layer(neurons, return_sequences=True, activation=activation))
        # model.add(Dropout(dropout))
        # model.add(Dense(1))
        # model.add(Activation(activation))

        # model.compile(optimizer="adam", loss=loss)
        # model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs)

    def make_predictions(self, n_days: int) -> np.array:
        dataset_total = pd.concat((self.train_data[-self.window:], self.test_data), axis=0)
        inputs = dataset_total.values.reshape(-1, 1)
        X_test = []
        for i in range(self.window, len(inputs)):
            X_test.append(inputs[i - self.window:i, 0])
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_stock_price = self.model.predict(X_test)
        return predicted_stock_price.reshape(1, -1)[0]

        # # 1
        # test_values = np.concatenate(
        #     (self.train_data.values[-self.window :], self.test_data.values)
        # )

        # X_test = np.array(
        #     [test_values[i - self.window : i] for i in range(self.window, len(test_values))]
        # )
        # # y_test = np.array([test_values[i] for i in range(self.window, len(test_values))])

        # X_test = np.reshape(X_test, (*X_test.shape, 1))

        # predictions = self.model.predict(X_test)

        # return np.array(predictions)

        # # 2
        # predictions = []
        # X_train_values = self.train_data[-self.window:].values

        # for _ in range(n_days):
        #     X_train = np.array(X_train_values).reshape(1, -1, 1)
        #     predicted_stock_price = self.model.predict(X_train)[0]
        #     predictions.append(predicted_stock_price[0])
        #     X_train_values = np.delete(X_train_values, 0)
        #     X_train_values = np.concatenate((X_train_values, predicted_stock_price))

        # return np.array(predictions)
