from preprocessing import DataPreprocessor
from segmentation import CustomerSegmentation

# Load and preprocess data
processor = DataPreprocessor("../data/retail_data.xlsx")

processor.load_data()
processor.clean_data()
processor.feature_engineering()

# Customer Segmentation
segment = CustomerSegmentation(processor.df)

segment.create_rfm()

segment.elbow_method()

segment.train_model()

segment.cluster_summary()

segment.customer_personas()

segment.business_recommendations()

segment.visualize_clusters()

segment.cluster_distribution()

segment.save_model()

segment.export_results()

print("\nCustomer Segmentation Module Completed Successfully!")