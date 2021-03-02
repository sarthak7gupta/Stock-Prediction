import numpy as np
import pandas as pd
from numpy import array
from sklearn.svm import SVR

from base_model import BaseModel


class SVM(BaseModel):
    window = 14

    def train(self) -> None:
        X = np.array(pd.to_numeric(self.train_data.index))
        y = self.train_data.values
        X_train = X.reshape(-1, 1)
        y_train = y.reshape(-1, 1)

        # X = self.train_data
        # y = X.shift(-self.window)
        # X_train = X.values.reshape(-1, 1)
        # y_train = y.values.reshape(-1, 1)

        self.model = SVR(
            kernel="rbf",
            C=1e6,
            gamma=0.01
        )
        self.model.fit(X_train, y_train)

    def make_predictions(self, n_days: int) -> array:
        X = np.array(pd.to_numeric(self.test_data.index))
        X_test = X.reshape(-1, 1)

        # X = self.scaler.fit_transform(self.test_data.values.reshape(-1, 1))
        # X_test = X.values.reshape(-1, 1)

        return self.model.predict(X_test)
