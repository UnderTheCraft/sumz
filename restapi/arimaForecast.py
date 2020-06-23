from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

from restapi.companyValues import CompanyValues


class ARIMAForecast:

    def __init__(self):
        print('ARIMA Forecast Object created')

    def make_forecast(self, df: pd.DataFrame, forecast_length: int):
        reversed(df)
        model = SARIMAX(df, order=(1, 0, 0), seasonal_order=(0, 1, 1, 4), seasonal=True)
        trained_model = model.fit()
        print(trained_model.summary())
        forecast = trained_model.forecast(forecast_length)

        return forecast
