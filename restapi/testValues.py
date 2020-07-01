from datetime import datetime

class TestValues:
    last_date = datetime(2019, 12, 31)
    risk_free_interest_rate = 1.5
    market_risk_premium = 7.5
    fcf_growth_rate = 0

    dates = [datetime(2019, 12, 31), datetime(2019, 9, 31)]
    fcf = [1000, 1200]
    currency = "USD"

    @staticmethod
    def getFcf():
        return TestValues.dates, TestValues.fcf, TestValues.currency

    @staticmethod
    def getInitialValues():
        return TestValues.last_date,\
               TestValues.risk_free_interest_rate,\
               TestValues.market_risk_premium,\
               TestValues.fcf_growth_rate
