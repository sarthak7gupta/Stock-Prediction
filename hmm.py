import itertools

import numpy as np
# import pandas as pd
from hmmlearn.hmm import GaussianHMM
from numpy import array

from base_model import BaseModel


class HMM(BaseModel):
    n_latency_days = 10

    def train(self) -> None:
        self.train = self.stock_data.iloc[:len(self.train_data), :]
        self.test = self.stock_data.iloc[-len(self.test_data):, :]

        self._compute_all_possible_outcomes(
            50, 10, 10)

        feature_vector = self._extract_features(self.train)

        self.model = GaussianHMM(n_components=5)
        self.model.fit(feature_vector)

    def make_predictions(self, n_days: int) -> array:
        predicted_close_prices = []

        for day_index in range(n_days):
            open_price = self.test.iloc[day_index]['open_price']
            predicted_frac_change, _, _ = self._get_most_probable_outcome(
                day_index)
            pred = open_price * (1 + predicted_frac_change)
            predicted_close_prices.append(pred)

        return predicted_close_prices

    @staticmethod
    def _extract_features(data):
        open_price = data['open_price'].values
        close_price = data['close_price'].values
        high_price = data['high_price'].values
        low_price = data['low_price'].values

        frac_change = (close_price - open_price) / open_price
        frac_high = (high_price - open_price) / open_price
        frac_low = (open_price - low_price) / open_price

        return np.column_stack((frac_change, frac_high, frac_low))

    def _compute_all_possible_outcomes(self, n_steps_frac_change,
                                       n_steps_frac_high, n_steps_frac_low):
        frac_change_range = np.linspace(-0.1, 0.1, n_steps_frac_change)
        frac_high_range = np.linspace(0, 0.1, n_steps_frac_high)
        frac_low_range = np.linspace(0, 0.1, n_steps_frac_low)

        self._possible_outcomes = np.array(list(itertools.product(
            frac_change_range, frac_high_range, frac_low_range)))

    def _get_most_probable_outcome(self, day_index):
        previous_data_start_index = max(0, day_index - self.n_latency_days)
        previous_data_end_index = max(0, day_index - 1)
        previous_data = self.test.iloc[previous_data_end_index: previous_data_start_index]
        previous_data_features = self._extract_features(
            previous_data)

        outcome_score = []
        for possible_outcome in self._possible_outcomes:
            total_data = np.row_stack(
                (previous_data_features, possible_outcome))
            outcome_score.append(self.model.score(total_data))
        most_probable_outcome = self._possible_outcomes[np.argmax(
            outcome_score)]

        return most_probable_outcome
