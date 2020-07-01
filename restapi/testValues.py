from datetime import datetime

class TestValues:
    last_date = datetime(2019, 12, 31)
    risk_free_interest_rate = 1.5
    market_risk_premium = 7.5
    fcf_growth_rate = 0
    beta_factor = 1
    tax_rate = 26
    currency = "USD"

    dates = [datetime(2019, 12, 31), datetime(2019, 9, 30)]
    yearly_future_fcfs = [1000, 1200]

    current_liability = 400
    yearly_future_liabilities = [500, 600]
    liabilities = [current_liability, *yearly_future_liabilities]
    last_quarterly_liability = 450

    @staticmethod
    def getFcf():
        return TestValues.dates, TestValues.fcf, TestValues.currency

    @staticmethod
    def getInitialValues():
        return TestValues.last_date,\
               TestValues.risk_free_interest_rate,\
               TestValues.market_risk_premium,\
               TestValues.fcf_growth_rate

    @staticmethod
    def calculateEnterpriseValue():
        enterprise_value = TestValues.calculatePresentValueOfCashFlow() + \
                           TestValues.calculatePresentValueOfTaxShield() - \
                           TestValues.getDebt()
        return enterprise_value

    @staticmethod
    def calculatePresentValueOfCashFlow():

        GKu = 0
        equity_interest = TestValues.calculateEquityInterest()
        print("Equity Interest: " + str(equity_interest))
        # Barwerte der zukünftigen Perioden berechnen
        for i in range(len(TestValues.yearly_future_fcfs) - 1):
            presentValue = TestValues.yearly_future_fcfs[i] / ((1 + equity_interest) ** (i + 1))
            GKu = GKu + presentValue
        print("GKu without residual value " + str(GKu))
        # Ewige Rente hinzufügen
        perpetuity = (equity_interest - TestValues.fcf_growth_rate / 100)
        if perpetuity <= 0:
            perpetuity = 1 / 100
        GKu = GKu + (TestValues.yearly_future_fcfs[-1]) / perpetuity
        print("GKu with residual value " + str(GKu))
        return GKu

    @staticmethod
    def calculatePresentValueOfTaxShield():
        tax_rate = TestValues.tax_rate / 100
        liability_interest = TestValues.risk_free_interest / 100
        Vs = 0
        # Barwerte des zukünfitgen FK berechnen
        for i in range(len(TestValues.yearly_future_liabilities - 1)):
            Vs = Vs + (tax_rate * liability_interest * TestValues.liabilities[i]) / ((1 + liability_interest) ** (i + 1))
        # "Ewiges Rentenmodell" für die FK berechnen
        Vs = Vs + (tax_rate * TestValues.liabilities[-1]) / ((1 + liability_interest) ** (len(TestValues.liabilities) - 1))
        print("Tax Shield " + str(Vs))
        return Vs

    @staticmethod
    def getDebt():
        return TestValues.last_quarterly_liability

    @staticmethod
    def calculateEquityInterest(self):
        equity_interest = TestValues.risk_free_interest_rate + \
                          (TestValues.market_risk_premium * \
                           TestValues.beta_factor)
        return equity_interest / 100
