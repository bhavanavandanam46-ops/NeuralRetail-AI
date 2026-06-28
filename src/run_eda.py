from preprocessing import DataPreprocessor
from eda import RetailEDA

processor = DataPreprocessor("../data/retail_data.xlsx")

processor.load_data()
processor.clean_data()
processor.feature_engineering()

eda = RetailEDA(processor.df)

eda.dataset_summary()
eda.sales_by_country()
eda.monthly_sales()
eda.top_products()