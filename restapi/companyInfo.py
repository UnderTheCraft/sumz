# The local company field is used if there are companies not available from the api,
# so that they are fetched from storage -> see companyValues.get_from_local
class CompanyInfo:
    def __init__(self):
        self.__local_companies_short = []  # ["SAP"]
        self.__api_companies_short = ["AAPL", "MSFT", "JNJ", "WMT", "V", "JPM", "PG", "UNH", "HD", "INTC", "VZ", "DIS",
                                      "MRK", "XOM",
                                      "KO", "PFE", "CSCO", "CVX", "MCD", "NKE", "IBM", "BA", "MMM", "AXP", "GS", "CAT",
                                      "WBA"
                                      "TRV"]  # ,"DOW","UTX"]
        self.__all_companies_short = self.__local_companies_short + self.__api_companies_short

        self.__local_companies_long = []  # ["SAP"]
        self.__api_companies_long = ["Apple", "Microsoft", "Johnson & Johnson", "Walmart", "Visa",
                                     "JP Morgan Chase & Co", "Procter & Gamble", "UnitedHealth Group", "The Home Depot",
                                     "Intel", "Verizon Communications", "The Walt Disney Co",
                                     "Merck", "Exxon Mobil",
                                     "Coca-Cola", "Pfizer", "Cisco Systems", "Chevron", "McDonalds", "Nike",
                                     "International Business Machines", "Boeing", "3M", "American Express",
                                     "Goldman Sachs", "Caterpillar",
                                     "Wallgreens Boots Alliance",
                                     "The Travellers Companies"]  # "Dow Inc","United Technologies Corporation"]
        self.__all_companies_long = self.__local_companies_long + self.__api_companies_long

        # TODO Combine all_companies_short with all_companies_long in dictionary
        # self.__all_companies_with_description =

    def get_all_companies(self):
        # TODO return self.__all_companies_with_description
        return {"companies": {"name": "AAPL", "description": "Apple"}}

    # def get_local_companies(self):
    #     return self.__local_companies_short

    def get_api_companies(self):
        return self.__api_companies_short
