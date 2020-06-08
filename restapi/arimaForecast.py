from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

class ARIMAForecast:

    def __init__(self):
        print('ARIMA Forecast Object created')

    def make_forecast(df: pd.DataFrame, prediction_length: int):
        model = SARIMAX(df, order=(1, 0, 0), seasonal_order=(0, 1, 1, 4), seasonal=True)
        trained_model = model.fit()
        forecast = trained_model.predict(prediction_length)

        return forecast
