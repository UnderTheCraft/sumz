class MarketValues:


    """ Risikoloser Zins:
    Kann anhand der Rendite von Staatsanleihen (30 Jahre) festgelegt werden.
    In diesem Fall sind dies US-Staatsanleihen, siehe https://www.investing.com/rates-bonds/u.s.-30-year-bond-yield
    Stand 06/2020: Risikoloser Zins standardmäßig auf 1.5 """
    __default__risk_free_interest = 1.5

    """ Marktrisikoprämie:
    Langfristige Entwicklung des Marktes - dem Risikolosen Zins.
    In diesem Fall hat der Dow Jones über 30 Jahre hinweg einen jährlichen Zuwachs von 9 %. """
    __default__market_risk_premium = 7.5

    """ International Tax Rates:
    https://home.kpmg/xx/en/home/services/tax/tax-tools-and-resources/tax-rates-online/corporate-tax-rates-table.html
    """
    __default_tax_rate = 21

    """ FCF Wachstumsrate:
    Prozentualer Wachstum des FCF im ewigen Rentenmodell
    """
    __default_fcf_growth_rate = 2.5

    def __init__(self, risk_free_interest: float = __default__risk_free_interest,
                 market_risk_premium: float = __default__market_risk_premium,
                 tax_rate: float = __default_tax_rate,
                 fcf_growth_rate: float = __default_fcf_growth_rate):

        self.__risk_free_interest = risk_free_interest
        self.__market_risk_premium = market_risk_premium
        self.__tax_rate = tax_rate
        self.__fcf_growth_rate = fcf_growth_rate

    def get_risk_free_interest(self):
        return self.__risk_free_interest

    def set_risk_free_interest(self, risk_free_interest: float):
        self.__risk_free_interest = risk_free_interest

    def get_market_risk_premium(self):
        return self.__market_risk_premium

    def set_market_risk_premium(self, market_risk_premium: float):
        self.__market_risk_premium = market_risk_premium

    def get_tax_rate(self):
        return self.__tax_rate

    def set_tax_rate(self, tax_rate: float):
        self.__tax_rate = tax_rate

    def get_fcf_growth_rate(self):
        return self.__fcf_growth_rate

    def set_fcf_growth_rate(self, fcf_growth_rate: float):
        self.__fcf_growth_rate = fcf_growth_rate
