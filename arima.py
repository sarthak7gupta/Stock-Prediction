from numpy import array
from pmdarima.arima import auto_arima

from base_model import BaseModel


class ARIMA(BaseModel):
    def train(self) -> None:
        self.model = auto_arima(
            self.train_data,
            d=1,
            start_p=1,
            start_q=1,
            max_p=5,
            max_q=5,
            start_P=0,
            start_Q=0,
            D=1,
            max_P=5,
            max_Q=5,
            m=12,
            seasonal=True,
            error_action="warn",
            trace=True,
            supress_warnings=True,
            stepwise=True,
            n_fits=30,
        )

    def make_predictions(self, n_days: int) -> array:
        return self.model.predict(n_periods=n_days)
