from restapi.baseMethod import BaseMethod
from restapi.arimaForecast import ARIMAForecast
from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues
from datetime import datetime
import numpy as np


class APV(BaseMethod):

    def __init__(self, company: str = None, last_date_forecast: datetime = None, risk_free_interest_rate: float = None,
                 market_risk_premium: float = None):
        self.company = company
        self.last_date_forecast = last_date_forecast
        self.companyValues = CompanyValues()
        self.marketValues = MarketValues()

        if risk_free_interest_rate is not None:
            self.marketValues.set_risk_free_interest(risk_free_interest_rate)
        if market_risk_premium is not None:
            self.marketValues.set_market_risk_premium(market_risk_premium)

    def calculateEnterpriseValue(self):
        enterprise_value = self.calculatePresentValueOfCashFlow() + \
                           self.calculatePresentValueOfTaxShield() - \
                           self.getDebt()

        return enterprise_value

    def calculatePresentValueOfCashFlow(self):

        dates, fcfs, currency = CompanyValues().get_cash_flows_array(self.company)

        self.currency = currency

        if self.last_date_forecast is None:
            self.last_date_forecast = dates[0]
            past_fcfs = fcfs[0:20]

        else:
            for date in dates:
                if date <= self.last_date_forecast:
                    index = dates.index(date)
                    self.last_date_forecast = date
                    break
            past_fcfs = fcfs[index:index+20]

        past_fcfs.reverse()

        self.number_of_values_for_forecast = len(past_fcfs)

        print("Past fcfs "+str(past_fcfs))

        forecast_fcfs_quarterly = ARIMAForecast().make_forecast(past_fcfs, 20)
        print("FCF quarterly "+str(forecast_fcfs_quarterly))

        forecast_fcfs_year = np.sum(np.array_split(forecast_fcfs_quarterly, 5), axis=1)
        print("FCF year" + str(forecast_fcfs_year))

        GKu = 0
        equity_interest = self.calculateEquityInterest()
        print("Equityinterest " + str(equity_interest))

        for i in range(len(forecast_fcfs_year) - 1):
            GKu = GKu + (forecast_fcfs_year / ((1 + equity_interest) ** i))

        GKu = forecast_fcfs_year[-1] / (equity_interest * (1 + equity_interest) ** len(forecast_fcfs_year))

        return GKu

    def calculatePresentValueOfTaxShield(self):
        return 0

    def getDebt(self):

        quarterly_liabilites = self.companyValues.get_quarterly_liabilities(self.company, as_json=True)
        for liability in quarterly_liabilites:
            print(liability["date"])
            try:
                liability_date = datetime.strptime(liability["date"], "%a, %b %m %Y %H:%M:%S %Z")
                last_date = datetime.strptime(self.last_date_forecast, "%d.%m.%Y")
                print(f"if {liability_date} < {last_date}: ")
                print(liability_date < last_date)
            except Exception as e:
                print("comparision not possible")

        return 0

    def calculateEquityInterest(self):
        equity_interest = self.marketValues.get_risk_free_interest() + \
                          (self.marketValues.get_market_risk_premium() * \
                           self.companyValues.get_beta_factor(self.company))

        return equity_interest/100

    def getAdditionalValues(self):

        additionalVaules = {"Number of values used for forecast": self.number_of_values_for_forecast,
                            "Date of last used past value": self.last_date_forecast,
                            "Currency": self.currency,
                            "recommendation":"BUY"
                            }

        return additionalVaules
