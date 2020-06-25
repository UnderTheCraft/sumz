from restapi.baseMethod import BaseMethod
from restapi.arimaForecast import ARIMAForecast
from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues
from datetime import datetime
import numpy as np
from math import floor

from restapi.recommendation import Recommendation


class APV(BaseMethod):

    def __init__(self, company: str = None, last_date: datetime = None,
                 risk_free_interest_rate: float = None, market_risk_premium: float = None):
        """ Die benötigten Parameter werden festgelegt """

        self.__company = company
        if last_date is None:
            self.__last_date = datetime.today().date()
        else:
            self.__last_date = last_date
        self.last_date_debt = None
        self.__companyValues = CompanyValues()
        self.__marketValues = MarketValues()

        self.__market_capitalization = self.__companyValues.get_market_capitalization(self.__company)

        # Wenn vom Anwender spezifische Parameter verwendet werden, werden diese in dem marketValues Objekt
        # überschrieben und bei Kalkulationen später verwendet
        if risk_free_interest_rate is not None:
            self.__marketValues.set_risk_free_interest(risk_free_interest_rate)
        if market_risk_premium is not None:
            self.__marketValues.set_market_risk_premium(market_risk_premium)

    def calculateEnterpriseValue(self):
        """ Hauptmethode für die Berechnung des Unternehmenswertes """

        enterprise_value = self.calculatePresentValueOfCashFlow() + \
                           self.calculatePresentValueOfTaxShield() - \
                           self.getDebt()

        return floor(enterprise_value)

    def calculatePresentValueOfCashFlow(self):
        """ Berechnung des Barwertes zukünftiger Cashflows durch Abzinsung """

        dates, fcfs, self.currency = CompanyValues().get_cash_flows(self.__company)

        if self.__last_date is None:
            self.last_date_forecast = dates[0]
            past_fcfs = fcfs[0:20]

        else:
            for date in dates:
                if date <= self.__last_date:
                    index = dates.index(date)
                    self.last_date_forecast = date
                    break
            past_fcfs = fcfs[index:index + 20]

        past_fcfs.reverse()

        self.number_of_values_for_forecast = len(past_fcfs)

        print("Past fcfs " + str(past_fcfs))

        forecast_fcfs_quarterly = ARIMAForecast().make_forecast(past_fcfs, 20)
        print("FCF quarterly forecast " + str(forecast_fcfs_quarterly))

        self.forecast_fcfs_year = np.sum(np.array_split(forecast_fcfs_quarterly, 5), axis=1)
        print("FCF year forecast " + str(self.forecast_fcfs_year))

        GKu = 0
        equity_interest = self.calculateEquityInterest()
        print("Equityinterest " + str(equity_interest))

        for i in range(len(self.forecast_fcfs_year) - 1):
            presentValue = self.forecast_fcfs_year[i] / ((1 + equity_interest) ** (i + 1))
            GKu = GKu + presentValue

        print("GKu without residual value " + str(GKu))

        GKu = GKu + (self.forecast_fcfs_year[-1]) / (equity_interest * ((1 + equity_interest) ** len(
            self.forecast_fcfs_year)))
        print("GKu with residual value " + str(GKu))


        return GKu

    def calculatePresentValueOfTaxShield(self):

        fk_fcf_ratio = self.calculateFkFcfRatio()
        print("FK FCF Ratio: "+str(fk_fcf_ratio))
        current_liability = self.getDebt()
        forecast_liabilities = np.multiply(self.forecast_fcfs_year[:-1], fk_fcf_ratio)
        liabilities = [current_liability,*forecast_liabilities]
        print("Liabilities: "+str(liabilities))

        tax_rate = self.__marketValues.get_tax_rate() / 100
        liability_interest = self.__marketValues.get_risk_free_interest() / 100

        Vs = 0

        for i in range(len(forecast_liabilities-1)):
            Vs = Vs + (tax_rate*liability_interest*liabilities[i])/((1+liability_interest)**(i+1))

        Vs = Vs + (tax_rate*liabilities[-1])/((1+liability_interest)**len(liabilities))

        print("Tax Shield " + str(Vs))

        return Vs

    def getDebt(self):
        """ Gibt das für ein bestimmtes Datum angegebenene quartalsweise Fremdkapital eines Unternehmens zurück """

        quarterly_liabilities = self.__companyValues.get_liabilities(self.__company, quarterly=True, as_json=True)

        for liability in quarterly_liabilities:
            if liability["date"] <= self.__last_date:
                last_liability = liability
            else:
                break

        self.last_date_debt = last_liability["date"]
        print(f"last date debt: {self.last_date_debt} and liability: {last_liability['liability']}")
        return last_liability["liability"]

    def calculateFkFcfRatio(self):

        annual_liabilities = self.__companyValues.get_liabilities(self.__company, quarterly=False, as_json=True)
        annual_cash_flows = self.__companyValues.get_annual_cash_flow(self.__company)

        fk_fcf_ratios = []

        for i in range(len(annual_liabilities)):
            if annual_liabilities[i]["date"] == annual_cash_flows[i]["date"] and annual_liabilities[i]["date"] <= self.__last_date:
                fk_fcf_ratios.append(annual_liabilities[i]["liability"]/annual_cash_flows[i]["cash flow"])
                self.last_date_fk_fcf_ratio = annual_liabilities[i]["date"]

        self.number_of_values_for_fk_fcf_ratio = len(fk_fcf_ratios)

        return np.average(fk_fcf_ratios)

    def calculateEquityInterest(self):
        """ Berechnung der Eigenkapitalverzinsung """

        equity_interest = self.__marketValues.get_risk_free_interest() + \
                          (self.__marketValues.get_market_risk_premium() * \
                           self.__companyValues.get_beta_factor(self.__company))

        return equity_interest / 100

    def getAdditionalValues(self, companyValue: float, percentage_deviation: float):
        """ Zusätzliche Parameter, welche zur Angabe des Unternehmenswerte benötigt werden """

        additionalVaules = {"Number of values used for forecast": self.number_of_values_for_forecast,
                            "Number of values used for FK FCF Ratio": self.number_of_values_for_fk_fcf_ratio,
                            "Date of last used past value": self.last_date_forecast,
                            "Date of last used FK FCF Ratio": self.last_date_fk_fcf_ratio,
                            "Date of debt used": self.last_date_debt,
                            "Currency": self.currency,
                            "Market Capitalization": self.__market_capitalization,
                            "Amount of Shares": self.__companyValues.get_amount_shares(self.__company),
                            "Recommendation": self.getRecommendation(companyValue, percentage_deviation)
                            }

        return additionalVaules

    def getRecommendation(self, companyValue: float, percentage_deviation: float):
        """ Methode für die Berechnung der Kaufempfehlung anhand berechnetem Wert und realer Marktkapitalisierung """

        # Untergrenze der Bewertung -> Liegt der berechnete Unternehmenswert darunter wird verkauft!
        floor = (self.__market_capitalization / 100) * (100 - percentage_deviation)
        # Obergrenze der Bewertung -> Liegt der berechnete Unternehmenswert darüber wird gekauft!
        ceiling = (self.__market_capitalization / 100) * (100 + percentage_deviation)

        if companyValue <= floor:
            return Recommendation.SELL.value
        elif companyValue >= ceiling:
            return Recommendation.BUY.value
        else:
            return Recommendation.HOLD.value
