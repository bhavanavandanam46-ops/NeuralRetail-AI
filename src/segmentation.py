"""
NeuralRetail AI
Customer Segmentation Module
----------------------------------------
Performs:
1. RFM Analysis
2. Elbow Method
3. KMeans Clustering
4. Customer Personas
5. Business Recommendations
6. Charts
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib


class CustomerSegmentation:

    def __init__(self, df):

        self.df = df.copy()
        self.rfm = None
        self.scaler = StandardScaler()
        self.model = None

    # -----------------------------------
    # Create RFM Table
    # -----------------------------------

    def create_rfm(self):

        latest_date = self.df["InvoiceDate"].max()

        self.rfm = self.df.groupby("CustomerID").agg(
            {
                "InvoiceDate": lambda x: (
                    latest_date - x.max()
                ).days,

                "Invoice": "nunique",

                "TotalSales": "sum"
            }
        )

        self.rfm.columns = [
            "Recency",
            "Frequency",
            "Monetary"
        ]

        print("\nRFM Table Created Successfully")

        return self.rfm

    # -----------------------------------
    # Scale Data
    # -----------------------------------

    def scale_data(self):

        scaled = self.scaler.fit_transform(
            self.rfm
        )

        return scaled

    # -----------------------------------
    # Elbow Method
    # -----------------------------------

    def elbow_method(self):

        scaled = self.scale_data()

        inertia = []

        K = range(2,11)

        for k in K:

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            model.fit(scaled)

            inertia.append(model.inertia_)

        plt.figure(figsize=(8,5))

        plt.plot(
            K,
            inertia,
            marker="o",
            linewidth=3
        )

        plt.title("Elbow Method")

        plt.xlabel("Number of Clusters")

        plt.ylabel("Inertia")

        plt.grid(alpha=0.3)

        plt.show()

    # -----------------------------------
    # Train KMeans
    # -----------------------------------

    def train_model(self):

        scaled = self.scale_data()

        self.model = KMeans(
            n_clusters=4,
            random_state=42,
            n_init=10
        )

        self.rfm["Cluster"] = self.model.fit_predict(
            scaled
        )

        print("\nModel Trained Successfully")

        return self.rfm
        # -----------------------------------
    # Cluster Summary
    # -----------------------------------

    def cluster_summary(self):

        summary = self.rfm.groupby("Cluster").agg(
            CustomerCount=("Cluster", "count"),
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("Monetary", "mean")
        )

        summary = summary.round(2)

        print("\n" + "="*60)
        print("CUSTOMER SEGMENT SUMMARY")
        print("="*60)

        print(summary)

        return summary

    # -----------------------------------
    # Customer Personas
    # -----------------------------------

    def customer_personas(self):

        summary = self.cluster_summary()

        personas = {}

        for cluster in summary.index:

            rec = summary.loc[cluster, "AvgRecency"]
            freq = summary.loc[cluster, "AvgFrequency"]
            money = summary.loc[cluster, "AvgMonetary"]

            if money > summary["AvgMonetary"].median() and freq > summary["AvgFrequency"].median():

                personas[cluster] = "Premium Customers"

            elif rec < summary["AvgRecency"].median():

                personas[cluster] = "Recent Customers"

            elif freq > summary["AvgFrequency"].median():

                personas[cluster] = "Loyal Customers"

            else:

                personas[cluster] = "Occasional Customers"

        print("\n" + "="*60)
        print("CUSTOMER PERSONAS")
        print("="*60)

        for cluster, persona in personas.items():

            print(f"Cluster {cluster} : {persona}")

        return personas

    # -----------------------------------
    # Business Recommendations
    # -----------------------------------

    def business_recommendations(self):

        personas = self.customer_personas()

        print("\n" + "="*60)
        print("BUSINESS RECOMMENDATIONS")
        print("="*60)

        for cluster, persona in personas.items():

            print(f"\nCluster {cluster}")

            if persona == "Premium Customers":

                print("✓ Offer VIP Membership")
                print("✓ Exclusive Discounts")
                print("✓ Early Product Access")

            elif persona == "Loyal Customers":

                print("✓ Loyalty Reward Program")
                print("✓ Bundle Offers")
                print("✓ Referral Rewards")

            elif persona == "Recent Customers":

                print("✓ Welcome Coupons")
                print("✓ Personalized Emails")
                print("✓ Product Recommendations")

            else:

                print("✓ Seasonal Discounts")
                print("✓ Flash Sales")
                print("✓ Re-engagement Campaign")
                    # -----------------------------------
    # Cluster Visualization
    # -----------------------------------

    def visualize_clusters(self):

        plt.figure(figsize=(10,7))

        sns.scatterplot(
            data=self.rfm,
            x="Frequency",
            y="Monetary",
            hue="Cluster",
            palette="Set2",
            s=90,
            edgecolor="black"
        )

        plt.title(
            "Customer Segmentation (RFM + KMeans)",
            fontsize=15
        )

        plt.xlabel("Purchase Frequency")
        plt.ylabel("Total Spending")

        plt.grid(alpha=0.3)

        plt.tight_layout()

        plt.show()

    # -----------------------------------
    # Cluster Distribution
    # -----------------------------------

    def cluster_distribution(self):

        plt.figure(figsize=(7,5))

        sns.countplot(
            x="Cluster",
            data=self.rfm,
            palette="Set2"
        )

        plt.title("Customers per Cluster")

        plt.tight_layout()

        plt.show()

    # -----------------------------------
    # Save Model
    # -----------------------------------

    def save_model(self):

        joblib.dump(
            self.model,
            "../models/customer_segmentation.pkl"
        )

        print("\nSegmentation model saved.")

    # -----------------------------------
    # Export Results
    # -----------------------------------

    def export_results(self):

        self.rfm.to_csv(
            "../reports/customer_segments.csv",
            index=True
        )

        print("Customer segments exported.")