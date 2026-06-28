"""
NeuralRetail AI
Customer Churn Prediction Module
--------------------------------
Predicts customer churn based on RFM analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


class CustomerChurn:

    def __init__(self, df):

        self.df = df.copy()
        self.rfm = None
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

    # -----------------------------
    # Create RFM
    # -----------------------------

    def create_dataset(self):

        latest_date = self.df["InvoiceDate"].max()

        self.rfm = self.df.groupby("CustomerID").agg({

            "InvoiceDate": lambda x:
                (latest_date - x.max()).days,

            "Invoice": "nunique",

            "TotalSales": "sum"

        })

        self.rfm.columns = [

            "Recency",

            "Frequency",

            "Monetary"

        ]

        print("RFM Dataset Created")

        return self.rfm

    # -----------------------------
    # Create Churn Labels
    # -----------------------------

    def create_target(self):

        self.rfm["Churn"] = (
            self.rfm["Recency"] > 90
        ).astype(int)

        print("Target Variable Created")

    # -----------------------------
    # Train Model
    # -----------------------------

    def train_model(self):

        X = self.rfm[[
            "Recency",
            "Frequency",
            "Monetary"
        ]]

        y = self.rfm["Churn"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,
            y,
            test_size=0.2,
            random_state=42

        )

        self.model.fit(

            X_train,
            y_train

        )

        prediction = self.model.predict(X_test)

        print("\nAccuracy")

        print(
            accuracy_score(
                y_test,
                prediction
            )
        )

        print("\nClassification Report")

        print(
            classification_report(
                y_test,
                prediction
            )
        )

        cm = confusion_matrix(
            y_test,
            prediction
        )

        plt.figure(figsize=(6,5))

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues"
        )

        plt.title(
            "Confusion Matrix"
        )

        plt.savefig(
            "../reports/churn_confusion_matrix.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Confusion Matrix Saved")
            # -----------------------------
    # Feature Importance
    # -----------------------------

    def feature_importance(self):

        importance = pd.DataFrame({
            "Feature": ["Recency", "Frequency", "Monetary"],
            "Importance": self.model.feature_importances_
        })

        importance = importance.sort_values(
            by="Importance",
            ascending=False
        )

        print("\nFeature Importance")
        print(importance)

        plt.figure(figsize=(8,5))

        sns.barplot(
            data=importance,
            x="Importance",
            y="Feature",
            hue="Feature",
            palette="viridis",
            legend=False
        )

        plt.title("Feature Importance")

        plt.savefig(
            "../reports/feature_importance.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        print("Feature Importance Chart Saved")

    # -----------------------------
    # Predict Churn
    # -----------------------------

    def predict_churn(self):

        X = self.rfm[
            ["Recency", "Frequency", "Monetary"]
        ]

        self.rfm["Prediction"] = self.model.predict(X)

        print("Predictions Generated")

    # -----------------------------
    # Save Model
    # -----------------------------

    def save_model(self):

        joblib.dump(
            self.model,
            "../models/churn_model.pkl"
        )

        print("Churn Model Saved")

    # -----------------------------
    # Export Results
    # -----------------------------

    def export_results(self):

        self.rfm.to_csv(
            "../reports/customer_churn_predictions.csv",
            index=True
        )

        print("Predictions Exported")