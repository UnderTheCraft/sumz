from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues


class APV:

    def __init__(self, company: str, risk_free_interest_rate: float = None, market_risk_premium: float = None):
        self.company = company
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
        return

    def calculatePresentValueOfTaxShield(self):
        return

    def getDebt(self):
        return

    def calculateEquityInterest(self):
        equity_interest = self.marketValues.set_risk_free_interest() + \
                          self.marketValues.get_market_risk_premium() * \
                          self.companyValues.get_beta_factor(self.company)

        return equity_interest
