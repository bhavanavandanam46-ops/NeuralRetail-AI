from preprocessing import DataPreprocessor


processor = DataPreprocessor(
    "../data/retail_data.xlsx"
)

processor.load_data()
processor.clean_data()
processor.feature_engineering()

processor.save_data(
    "../data/clean_retail_data.csv"
)

print(processor.df.head())

print("\nDataset Shape:")
print(processor.df.shape)