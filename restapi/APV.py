from restapi.companyValues import CompanyValues


class APV:

    def __init__(self, company: str, riskfreeInterestRate, marketRiskPremium):
        self.company = company
        self.riskfreeInterestRate = riskfreeInterestRate
        self.marketRiskPremium = marketRiskPremium
        self.companyValues = CompanyValues()

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
        equity_interest = self.riskfreeInterestRate + \
                          self.marketRiskPremium * \
                          self.companyValues.get_beta_factor(self.company)

        return equity_interest
