
class CompanyInfo:
    def __init__(self):
        self.__all_companies_short = ["AAPL", "MSFT", "JNJ", "WMT", "V", "JPM", "PG", "UNH", "HD", "INTC", "VZ", "DIS",
                                      "MRK", "XOM",
                                      "KO", "PFE", "CSCO", "CVX", "MCD", "NKE", "IBM", "BA", "MMM", "AXP", "GS", "CAT",
                                      "WBA"
                                      "TRV"]  # ,"DOW","UTX"]

        self.__all_companies_long = ["Apple", "Microsoft", "Johnson & Johnson", "Walmart", "Visa",
                                     "JP Morgan Chase & Co", "Procter & Gamble", "UnitedHealth Group", "The Home Depot",
                                     "Intel", "Verizon Communications", "The Walt Disney Co",
                                     "Merck", "Exxon Mobil",
                                     "Coca-Cola", "Pfizer", "Cisco Systems", "Chevron", "McDonalds", "Nike",
                                     "International Business Machines", "Boeing", "3M", "American Express",
                                     "Goldman Sachs", "Caterpillar",
                                     "Wallgreens Boots Alliance",
                                     "The Travellers Companies"]  # "Dow Inc","United Technologies Corporation"]

        self.__all_companies_with_description = [{"short_name": short_name, "long_name": long_name} for
                                                 short_name, long_name in
                                                 zip(self.__all_companies_short, self.__all_companies_long)]

    def get_all_companies(self):
        return self.__all_companies_with_description
