import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class RetailEDA:

    def __init__(self, dataframe):
        self.df = dataframe

    def dataset_summary(self):

        print("="*60)
        print("NEURALRETAIL DATA SUMMARY")
        print("="*60)

        print("\nShape:")
        print(self.df.shape)

        print("\nColumns:")
        print(self.df.columns.tolist())

        print("\nMissing Values:")
        print(self.df.isnull().sum())

    def sales_by_country(self):

        country_sales = (
            self.df.groupby("Country")["TotalSales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(12,6))
        sns.barplot(
            x=country_sales.values,
            y=country_sales.index
        )

        plt.title("Top 10 Countries by Revenue")
        plt.tight_layout()
        plt.show()

    def monthly_sales(self):

        monthly = (
            self.df.groupby("Month")["TotalSales"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly,
            x="Month",
            y="TotalSales",
            markers=True,
            title="Monthly Revenue Trend"
        )

        fig.show()

    def top_products(self):

        products = (
            self.df.groupby("Description")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        plt.figure(figsize=(12,6))
        sns.barplot(
            x=products.values,
            y=products.index
        )

        plt.title("Top Selling Products")
        plt.tight_layout()
        plt.show()