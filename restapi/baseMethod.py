from abc import abstractmethod
from datetime import datetime, date

from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues


class BaseMethod:

    def __init__(self, company:str, last_date: date = None, risk_free_interest_rate: float = None, market_risk_premium: float = None):

        """ Die benötigten Parameter werden festgelegt """

        self.__company = company

        if last_date is None:
            self.__last_date = datetime.today().date()
        else:
            self.__last_date = last_date

        # Wenn vom Anwender spezifische Parameter verwendet werden, werden diese in dem marketValues Objekt
        # überschrieben und bei Kalkulationen später verwendet
        if risk_free_interest_rate is not None:
            self.__marketValues.set_risk_free_interest(risk_free_interest_rate)
        if market_risk_premium is not None:
            self.__marketValues.set_market_risk_premium(market_risk_premium)

        self.__companyValues = CompanyValues()
        self.__marketValues = MarketValues()

        self.__market_capitalization, self.__amount_shares = \
            self.__companyValues.get_market_capitalization_and_amount_shares(company)

        print(f"Initialized Calculation Method:\n  Company: {self.__company}\n  Last Date: {self.__last_date}"
              f"\n  Risk Free Interest Rate: {self.__risk_free_interest_rate}\n  Market Risk Premium: {self.__market_risk_premium}")


    @abstractmethod
    def calculateEnterpriseValue(self):
        pass

    @abstractmethod
    def getAdditionalValues(self):
        pass
