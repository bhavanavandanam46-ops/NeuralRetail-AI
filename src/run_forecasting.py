from preprocessing import DataPreprocessor
from forecasting import DemandForecast

processor = DataPreprocessor("../data/retail_data.xlsx")

processor.load_data()
processor.clean_data()
processor.feature_engineering()

forecast = DemandForecast(processor.df)

forecast.prepare_data()

forecast.train()

forecast.forecast_next()

forecast.plot_forecast()

forecast.save_model()

forecast.export()

print("\nDemand Forecasting Completed Successfully!")