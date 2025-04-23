from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np

# Inherited model: Used for evaluation and organization
class SequenceModel(BaseEstimator):
    def print_report(self, X_test, y_test):
        print("report")
        # TODO


# Simplest model: Predicts solely from the last datapoint
class PointPredictor(SequenceModel):
    def __init__(self, regressor, scaler=None):
        self.regressor = regressor
        self.scaler = scaler or StandardScaler()
        if scaler is None:
            self.scaler_unfit = True
        else:
            self.scaler_unfit = False

    def _preprocess(self, X):
        copy = X.copy(deep=True)

        copy[self.feature_names] = self.scaler.transform(X[self.feature_names])
        return copy

    def fit(self, X, preprocess=True):
        copy = X.copy(deep=True)
        y = X.groupby('unit')['cycle'].transform(lambda x: x.max() - x)

        features = [col for col in copy.columns if col not in ['unit', 'cycle', 'RUL', 'failure_30']]
        self.feature_names = features
        copy = copy[features]

        if self.scaler_unfit:
            self.scaler.fit(copy)

        if preprocess:
            copy = self._preprocess(copy)

        self.regressor.fit(copy, y)
        return self

    def predict(self, X, preprocess=True):
        if isinstance(X, list):
            datapoints = [x[self.feature_names].iloc[-1] for x in X]
        else:
            datapoints = X.groupby('unit').tail(1)[self.feature_names]

        if preprocess:
            datapoints = self._preprocess(datapoints)

        return self.regressor.predict(datapoints)

class PointPredictorRegressor(SequenceModel):
    def __init__(self, regressor, scaler=None):
        self.regressor = regressor
        self.scaler = scaler or StandardScaler()
        self.scaler_unfit = scaler is None

    def _preprocess(self, X):
        copy = X.copy(deep=True)

        copy[self.feature_names] = self.scaler.transform(X[self.feature_names])
        return copy

    def fit(self, X, preprocess=True):
        copy = X.copy(deep=True)
        y = X.groupby('unit')['cycle'].transform(lambda x: x.max() - x)

        features = [col for col in copy.columns if col not in ['unit', 'cycle', 'RUL', 'failure_30']]
        self.feature_names = features
        copy = copy[features]

        if self.scaler_unfit:
            self.scaler.fit(copy)

        if preprocess:
            copy = self._preprocess(copy)

        self.regressor.fit(copy, y)
        return self

    def predict(self, X, preprocess=True, end_points=10):
        if isinstance(X, list):
            sequences = [self._preprocess(x[self.feature_names]) if preprocess else x[self.feature_names] for x in X]
        else:
            df = self._preprocess(X) if preprocess else X.copy(deep=True)
            sequences = [group for _, group in df.groupby('unit')[self.feature_names]]

        ret = []
        for sequence in sequences:
            if end_points > 0:
                sequence = sequence[-end_points:]

            rul_pred = self.regressor.predict(sequence)

            x = np.arange(rul_pred.shape[0]).reshape(-1, 1)
            linModel = LinearRegression()
            linModel.fit(x, rul_pred)

            ret.append(linModel.predict(np.array([[rul_pred.shape[0]]]))[0])  # get scalar
        return ret
