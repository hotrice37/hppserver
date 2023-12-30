from sklearn.ensemble import RandomForestRegressor


class RandomForestModel:
    def __init__(self):
        self.model = RandomForestRegressor()
        self.feature_names = None

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        self.feature_names = X_train.columns.tolist()

    def predict(self, X_test):
        return self.model.predict(X_test)
