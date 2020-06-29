from abc import abstractmethod
from datetime import datetime, date

from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues


class BaseMethod:

    def __init__(self, company: str, last_date: date = None, risk_free_interest_rate: float = None,
                 market_risk_premium: float = None, fcf_growth_rate: float = None):

        """ Die benötigten Parameter werden festgelegt """

        self._company = company
        self._companyValues = CompanyValues()
        self._marketValues = MarketValues()

        if last_date is None:
            self._last_date = datetime.today().date()
        else:
            self._last_date = last_date

        # Wenn vom Anwender spezifische Parameter verwendet werden, werden diese in dem marketValues Objekt
        # überschrieben und bei Kalkulationen später verwendet
        if risk_free_interest_rate is not None:
            self._marketValues.set_risk_free_interest(risk_free_interest_rate)
        if market_risk_premium is not None:
            self._marketValues.set_market_risk_premium(market_risk_premium)
        if fcf_growth_rate is not None:
            self._marketValues.set_fcf_growth_rate(fcf_growth_rate)

        self._market_capitalization, self._amount_shares = \
            self._companyValues.get_market_capitalization_and_amount_shares(company)

        print(f"Initialized Calculation Method:\n  Company: {self._company}\n  Last Date: {self._last_date}"
              f"\n  Risk Free Interest Rate: {self._marketValues.get_risk_free_interest()}\n  Market Risk Premium: {self._marketValues.get_market_risk_premium()}")


    @abstractmethod
    def calculateEnterpriseValue(self):
        pass

    @abstractmethod
    def getAdditionalValues(self):
        pass
