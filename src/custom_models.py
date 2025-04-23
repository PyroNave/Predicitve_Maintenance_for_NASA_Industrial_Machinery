from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler

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

    def predict(self, X, preprocess=True):
        if isinstance(X, list):
            datapoints = [x[self.feature_names].iloc[-1] for x in X]
        else:
            datapoints = X.groupby('unit').tail(1)[self.feature_names]

        if preprocess:
            datapoints = self._preprocess(datapoints)

        return self.regressor.predict(datapoints)
