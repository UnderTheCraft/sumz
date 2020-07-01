from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd



class ARIMAForecast:

    def __init__(self):
        print('ARIMA Forecast Object created')

    def make_forecast(self, df: pd.DataFrame, forecast_length: int):
        model = SARIMAX(df, order=(1, 0, 0), seasonal_order=(0, 1, 1, 4), enforce_stationarity=False, enforce_invertibility=True)
        trained_model = model.fit()
        print(trained_model.summary())
        forecast = trained_model.forecast(forecast_length)

        return forecast
