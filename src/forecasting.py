"""
NeuralRetail AI
Demand Forecasting Module
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import joblib


class DemandForecast:

    def __init__(self, df):

        self.df = df.copy()
        self.monthly_sales = None
        self.model = LinearRegression()

    # ---------------------------------------
    # Monthly Sales
    # ---------------------------------------

    def prepare_data(self):

        self.monthly_sales = (
            self.df.groupby(["Year", "Month"])["TotalSales"]
            .sum()
            .reset_index()
        )

        self.monthly_sales["TimeIndex"] = range(
            1,
            len(self.monthly_sales) + 1
        )

        print("\nMonthly sales prepared.")

        return self.monthly_sales

    # ---------------------------------------
    # Train Model
    # ---------------------------------------

    def train(self):

        X = self.monthly_sales[["TimeIndex"]]
        y = self.monthly_sales["TotalSales"]

        self.model.fit(X, y)

        self.monthly_sales["Prediction"] = self.model.predict(X)

        print("Forecast model trained.")

    # ---------------------------------------
    # Forecast Next Month
    # ---------------------------------------

    def forecast_next(self):

        next_month = len(self.monthly_sales) + 1

        prediction = self.model.predict([[next_month]])[0]

        print("\nPredicted Sales Next Month")

        print(f"₹ {prediction:,.2f}")

        return prediction

    # ---------------------------------------
    # Plot
    # ---------------------------------------

    def plot_forecast(self):

        plt.figure(figsize=(12,6))

        plt.plot(
            self.monthly_sales["TimeIndex"],
            self.monthly_sales["TotalSales"],
            marker="o",
            label="Actual Sales"
        )

        plt.plot(
            self.monthly_sales["TimeIndex"],
            self.monthly_sales["Prediction"],
            linestyle="--",
            linewidth=3,
            label="Trend"
        )

        plt.title("Monthly Sales Forecast")

        plt.xlabel("Month")

        plt.ylabel("Revenue")

        plt.legend()

        plt.grid(alpha=0.3)

        plt.savefig(
            "../reports/monthly_forecast.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

    # ---------------------------------------
    # Save
    # ---------------------------------------

    def save_model(self):

        joblib.dump(
            self.model,
            "../models/forecast_model.pkl"
        )

        print("Forecast model saved.")

    def export(self):

        self.monthly_sales.to_csv(
            "../reports/monthly_forecast.csv",
            index=False
        )

        print("Forecast exported.")