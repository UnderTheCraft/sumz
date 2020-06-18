from restapi.companyValues import CompanyValues


class APV:

    def __init__(self,company,riskfreeInterestRate,marktetRiskPremium):
        self.company = company
        self.riskfreeInterestRate = riskfreeInterestRate
        self.marketRiskPremium = marktetRiskPremium
        self.companyValues = CompanyValues()


    def calculateEnterpriseValue(self):

        enterpriseValue = self.calculatePresentValueOfCashFlow() + self.calculatePresentValueOfTaxShield() - self.getDebt()

        return enterpriseValue

    def calculatePresentValueOfCashFlow(self):

        return

    def calculatePresentValueOfTaxShield(self):
        return

    def getDebt(self):
        return

    def calculateEquityInterest(self):

        equityInterest = self.riskfreeInterestRate + self.marketRiskPremium * self.companyValues.get_beta_factor(self.company)

        return equityInterest