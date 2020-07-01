from restapi.baseMethod import BaseMethod
from restapi.arimaForecast import ARIMAForecast
from restapi.companyValues import CompanyValues
from restapi.testValues import TestValues
from datetime import date
import numpy as np
from math import floor

from restapi.recommendation import Recommendation


class APV(BaseMethod):
    """ Implementiert das Adjusted-Present-Value Verfahren """

    def __init__(self, company: str, last_date: date = None, risk_free_interest_rate: float = None,
                 market_risk_premium: float = None, fcf_growth_rate: float = None):
        # Aufruf der init in der Oberklasse (BaseMethod)
        super().__init__(company=company, last_date=last_date, risk_free_interest_rate=risk_free_interest_rate,
                         market_risk_premium=market_risk_premium, fcf_growth_rate=fcf_growth_rate)
        self.last_date_debt = None

    def calculateEnterpriseValue(self):
        """ Hauptmethode für die Berechnung des Unternehmenswertes """

        enterprise_value = self.calculatePresentValueOfCashFlow() + \
                           self.calculatePresentValueOfTaxShield() - \
                           self.getDebt()

        return floor(enterprise_value)

    def calculatePresentValueOfCashFlow(self):
        """ Berechnung des Barwertes zukünftiger Cashflows durch Abzinsung """

        if "TEST".__eq__(self._company):
            dates, fcfs, self.currency = TestValues.getFcf()
        else:
            dates, fcfs, self.currency = CompanyValues().get_cash_flows(self._company)

        if self._last_date is None:
            self.last_date_forecast = dates[0]
            self.past_fcfs = fcfs[0:20]
            self.past_dates = dates[0:20]

        else:
            for date in dates:
                if date <= self._last_date:
                    index = dates.index(date)
                    self.last_date_forecast = date
                    break
            self.past_fcfs = fcfs[index:index + 20]
            self.past_dates = dates[index:index + 20]

        self.past_dates.reverse()
        self.past_fcfs.reverse()

        self.number_of_values_for_forecast = len(self.past_fcfs)

        print("Past fcfs " + str(self.past_fcfs))

        self.forecast_fcfs_quarterly = ARIMAForecast().make_forecast(self.past_fcfs, 20)
        print("FCF quarterly forecast " + str(self.forecast_fcfs_quarterly))

        self.forecast_fcfs_year = np.sum(np.array_split(self.forecast_fcfs_quarterly, 5), axis=1)
        print("FCF year forecast " + str(self.forecast_fcfs_year))

        GKu = 0
        equity_interest = self.calculateEquityInterest()
        print("Equityinterest " + str(equity_interest))

        # Barwerte der zukünftigen Perioden berechnen
        for i in range(len(self.forecast_fcfs_year) - 1):
            presentValue = self.forecast_fcfs_year[i] / ((1 + equity_interest) ** (i + 1))
            GKu = GKu + presentValue

        print("GKu without residual value " + str(GKu))

        # Ewige Rente hinzufügen
        perpetuity = (equity_interest - self._marketValues.get_fcf_growth_rate() / 100)
        if perpetuity <= 0:
            perpetuity = 1 / 100
        GKu = GKu + (self.forecast_fcfs_year[-1]) / perpetuity
        print("GKu with residual value " + str(GKu))

        return GKu

    def calculatePresentValueOfTaxShield(self):
        """ Berechnung des Wertes, welcher durch den Tax Shield generiert wird """

        fk_fcf_ratio = self.calculateFkFcfRatio()
        print("FK FCF Ratio: " + str(fk_fcf_ratio))
        current_liability = self.getDebt()
        forecast_liabilities = np.multiply(self.forecast_fcfs_year[:-1], fk_fcf_ratio)
        liabilities = [current_liability, *forecast_liabilities]
        print("Liabilities: " + str(liabilities))

        tax_rate = self._marketValues.get_tax_rate() / 100
        liability_interest = self._marketValues.get_risk_free_interest() / 100

        Vs = 0

        # Barwerte des zukünfitgen FK berechnen
        for i in range(len(forecast_liabilities - 1)):
            Vs = Vs + (tax_rate * liability_interest * liabilities[i]) / ((1 + liability_interest) ** (i + 1))

        # "Ewiges Rentenmodell" für die FK berechnen
        Vs = Vs + (tax_rate * liabilities[-1]) / ((1 + liability_interest) ** (len(liabilities)-1))

        print("Tax Shield " + str(Vs))

        return Vs

    def getDebt(self):
        """ Gibt das letzte quartalsweise Fremdkapital eines Unternehmens zurück """

        quarterly_liabilities = self._companyValues.get_liabilities(self._company, quarterly=True, as_json=True)

        for liability in quarterly_liabilities:
            if liability["date"] <= self._last_date:
                last_liability = liability
            else:
                break

        self.last_date_debt = last_liability["date"]
        print(f"last date debt: {self.last_date_debt} and liability: {last_liability['liability']}")
        return last_liability["liability"]

    def calculateFkFcfRatio(self):
        """ Verhältnis zwischen FK und FCF:
        Wird verwendet, um die Werte des zukünfitgen FK zu schätzen
        """

        annual_liabilities = self._companyValues.get_liabilities(self._company, quarterly=False, as_json=True)
        annual_cash_flows = self._companyValues.get_annual_cash_flow(self._company)

        fk_fcf_ratios = []

        for i in range(len(annual_liabilities)):
            if annual_liabilities[i]["date"] == annual_cash_flows[i]["date"] and annual_liabilities[i][
                "date"] <= self._last_date:
                fk_fcf_ratios.append(annual_liabilities[i]["liability"] / annual_cash_flows[i]["cash flow"])
                self.last_date_fk_fcf_ratio = annual_liabilities[i]["date"]

        self.number_of_values_for_fk_fcf_ratio = len(fk_fcf_ratios)

        return np.average(fk_fcf_ratios)

    def calculateEquityInterest(self):
        """ Berechnung der Eigenkapitalverzinsung (CAPM Modell) """

        equity_interest = self._marketValues.get_risk_free_interest() + \
                          (self._marketValues.get_market_risk_premium() * \
                           self._companyValues.get_beta_factor(self._company))

        return equity_interest / 100

    def getAdditionalValues(self, companyValue: float, percentage_deviation: float):
        """ Zusätzliche Parameter, welche zur Angabe des Unternehmenswerte benötigt werden """

        forecast_dates = [self.past_dates[-1] + relativedelta(months=+(3*(i+1))) for i in range(len(self.forecast_fcfs_quarterly))]

        additionalVaules = {"Number of values used for forecast": self.number_of_values_for_forecast,
                            "Number of values used for FK FCF Ratio": self.number_of_values_for_fk_fcf_ratio,
                            "Date of last used past value": self.last_date_forecast,
                            "Date of last used FK FCF Ratio": self.last_date_fk_fcf_ratio,
                            "Date of debt used": self.last_date_debt,
                            "Currency": self.currency,
                            "Market Capitalization": self._market_capitalization,
                            "Amount of Shares": self._amount_shares,
                            "Recommendation": self.getRecommendation(companyValue, percentage_deviation),
                            "FCF": {
                                "Past": [{'date': date, 'FCF': fcf} for date, fcf in zip(self.past_dates, self.past_fcfs) ],
                                "Forecast":  [{'date': date, 'FCF': floor(fcf)} for date, fcf in zip(forecast_dates, self.forecast_fcfs_quarterly)]
                            }
                            }

        return additionalVaules

    def getRecommendation(self, companyValue: float, percentage_deviation: float):
        """ Methode für die Berechnung der Kaufempfehlung anhand berechnetem Wert und realer Marktkapitalisierung """

        # Untergrenze der Bewertung -> Liegt der berechnete Unternehmenswert darunter wird verkauft!
        floor = (self._market_capitalization / 100) * (100 - percentage_deviation)
        # Obergrenze der Bewertung -> Liegt der berechnete Unternehmenswert darüber wird gekauft!
        ceiling = (self._market_capitalization / 100) * (100 + percentage_deviation)

        if companyValue <= floor:
            return Recommendation.SELL.value
        elif companyValue >= ceiling:
            return Recommendation.BUY.value
        else:
            return Recommendation.HOLD.value
