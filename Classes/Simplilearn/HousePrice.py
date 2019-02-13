# coding=utf-8
# !/usr/bin/env python
# Bonus Exercise: Predict housing prices based on median_income and plot the regression chart.


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
pd.set_option('display.max_columns', None)


class PredictHousePrice(object):

    def __init__(self, input_file):

        self.input_file = input_file
        self.house_price = None
        self.X = None
        self.y = None
        self.cat = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None
        self.model = None

    def load_data(self):

        house_price = pd.read_csv(self.input_file,  na_values='NAN')
        house_price['ocean_proximity'] = house_price['ocean_proximity'].str.replace('<', '')
        house_price['total_bedrooms'] = house_price['total_bedrooms'].fillna(
            value=house_price['total_bedrooms'].mean())
        self.house_price = house_price
        self.house_price.hist(bins=50, figsize=(20, 10))
        plt.show()
        X = house_price.iloc[:, 1:len(house_price)]
        y = house_price.iloc[:, 0:1]

        self.X = X
        self.y = y

    def encode_categorical_data(self):
        cat = pd.get_dummies(data=self.X)
        self.cat = cat

    def train_test_split(self):
        X_train, X_test, y_train, y_test = train_test_split(self.cat, self.y, test_size=0.2, random_state=42)
        print(X_train.shape)
        print(X_test.shape)
        print(y_train.shape)
        print(y_test.shape)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def linear_reg(self):
        lm = LinearRegression()
        model_lm = lm.fit(self.X_train, self.y_train)
        predictions = lm.predict(self.X_test)
        print(predictions[0:5])

        self.predictions = predictions
        self.model = model_lm

    def plotting(self):
        plt.scatter(self.y_test, self.predictions)
        plt.xlabel('True Value')
        plt.ylabel('Predictions')
        print("Test score: ", self.model.score(self.X_test, self.y_test))
        print("Train score: ", self.model.score(self.X_train, self.y_train))
        plt.show()
        """plt.savefig()"""

    def main(self):
        self.load_data()
        self.encode_categorical_data()
        self.train_test_split()
        self.linear_reg()
        self.plotting()
        # self.poly_reg()


if __name__ == "__main__":
    path = "C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Simplilearn/Problems/Projects/" \
           "Projects for submission/California Housing Price Prediction/Dataset for the project/"
    obj = PredictHousePrice(path + 'housing.csv')
    obj.main()