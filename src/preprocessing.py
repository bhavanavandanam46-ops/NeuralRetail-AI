import pandas as pd


class DataPreprocessor:
    """
    Handles loading, cleaning and feature engineering
    for the NeuralRetail dataset.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        """Load Excel dataset"""
        self.df = pd.read_excel(self.filepath)
        return self.df

    def clean_data(self):
        """Clean retail dataset"""

        self.df.columns = [
            "Invoice",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country"
        ]

        self.df.dropna(subset=["CustomerID"], inplace=True)

        self.df = self.df[
            ~self.df["Invoice"].astype(str).str.startswith("C")
        ]

        self.df = self.df[self.df["Quantity"] > 0]
        self.df = self.df[self.df["UnitPrice"] > 0]

        return self.df

    def feature_engineering(self):

        self.df["InvoiceDate"] = pd.to_datetime(
            self.df["InvoiceDate"]
        )

        self.df["TotalSales"] = (
            self.df["Quantity"] *
            self.df["UnitPrice"]
        )

        self.df["Year"] = self.df["InvoiceDate"].dt.year
        self.df["Month"] = self.df["InvoiceDate"].dt.month
        self.df["Day"] = self.df["InvoiceDate"].dt.day
        self.df["Weekday"] = self.df["InvoiceDate"].dt.day_name()

        return self.df

    def save_data(self, output_path):
        self.df.to_csv(output_path, index=False)