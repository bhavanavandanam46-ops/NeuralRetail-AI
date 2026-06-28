from preprocessing import DataPreprocessor
from churn import CustomerChurn

# Load data
processor = DataPreprocessor("../data/retail_data.xlsx")

processor.load_data()
processor.clean_data()
processor.feature_engineering()

# Churn Prediction
churn = CustomerChurn(processor.df)

churn.create_dataset()

churn.create_target()

churn.train_model()

churn.feature_importance()

churn.predict_churn()

churn.save_model()

churn.export_results()

print("\nCustomer Churn Module Completed Successfully!")