from requests_html import HTMLSession
import requests
import pandas as pd
import traceback
from restapi.companyInfo import CompanyInfo
from dateutil import parser
from datetime import datetime
import time
from matplotlib import pyplot as plt
from io import BytesIO
from PIL import Image
import json

class CompanyValues:

    def __init__(self):
        self.__companies = CompanyInfo()
        self.__abbrevationToNumber = {'K': 3, 'M': 6, 'B': 9, 'T': 12}


    def get_cash_flows(self, company, as_json = False):

        try:

            session = HTMLSession()

            # TODO hier könnte ne tryExcept hin, falls z.b. keine Verbindung aufgebaut werden kann
            response = session.get(f'https://ycharts.com/companies/{company}/free_cash_flow')

            print(f"The headers of the requests are:\n{response.headers}")

            # TODO Zweite spalte mit cashflows sollte auch noch berücksichtigt werden
            raw_dates = response.html.find(".histDataTable", first=True).find(".col1")[1:]
            raw_fcfs = response.html.find(".histDataTable", first=True).find(".col2")[1:]
            currency = response.html.find("#securityQuote", first=True).find(".info")[1].text

            dates = [parser.parse(rawDate.text).date() for rawDate in raw_dates]
            fcfs = [int(float(rawFCF.text[:-1]) * 10 ** self.__abbrevationToNumber[rawFCF.text[-1]]) for rawFCF in raw_fcfs]

            if as_json:
                result_json = [{'date': date, 'FCF': fcf} for date, fcf in zip(dates, fcfs)]
                return [{"Free Cash Flows": result_json}, {"currency": currency}]
            else:
                return dates,fcfs,currency

        except Exception as e:
            print(f"{company} not available within API!")
            traceback.print_exc()


    def get_annual_cash_flow(self, company):

        try:
            period2 = str(int(time.time()))
            response = requests.get(f"https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{company}?type=%20%2CannualFreeCashFlow&period1=493590046&period2={period2}&corsDomain=finance.yahoo.com").json()
            result = response["timeseries"]["result"][0]
            dates = [datetime.fromtimestamp(timestamp) for timestamp in result["timestamp"]]
            cash_flow_objects = result["annualFreeCashFlow"]

            cash_flows = [cash_flow_object["reportedValue"]["raw"] for cash_flow_object in cash_flow_objects]

            return [{'date': date.date(), 'cash flow': cash_flow} for date, cash_flow in zip(dates, cash_flows)]

        except Exception as e:
            print(f"{company} not available within API!")
            traceback.print_exc()

    # get beta factor
    def get_beta_factor(self, company: str):
        try:
            session = HTMLSession()
            response = session.get(f'https://finance.yahoo.com/quote/{company}')
            beta_factor = response.html.find("[data-test='BETA_5Y-value']", first=True).text
            return float(beta_factor)

        except Exception as e:
            print(f"beta factor of company {company} not available within API!")
            traceback.print_exc()

    # get Liablilities (Fremdkapital)
    def get_liabilities(self,company:str,quarterly = False,as_json = False):
        try:
            frequency = "quarterly" if quarterly else "annual"

            period2 = str(int(time.time()))
            response = requests.get(f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{company}"
                                    f"?type=%2C{frequency}TotalLiabilitiesNetMinorityInterest&period1"
                                    f"=493590046&period2={period2}&corsDomain=finance.yahoo.com").json()
            result = response["timeseries"]["result"][0]
            dates = [datetime.fromtimestamp(timestamp) for timestamp in result["timestamp"]]
            liability_objects = result[f"{frequency}TotalLiabilitiesNetMinorityInterest"]

            liabilities = [liability_object["reportedValue"]["raw"] for liability_object in liability_objects]

            if as_json:
                return [{'date': date.date(), 'liability': liability} for date, liability in zip(dates, liabilities)]
            else:
                return dates, liabilities

        except Exception as e:
            print(f"liabilities of company {company} not available within API!")
            traceback.print_exc()

    # Markkapitalisierung
    def get_market_capitalization(self, company: str):
        try:
            session = HTMLSession()
            response = session.get(f'https://finance.yahoo.com/quote/{company}')
            market_cap = response.html.find("[data-test=MARKET_CAP-value]", first=True).text

            number = market_cap[:-1]
            abbr = market_cap[-1]

            return float(number) * 10 ** self.__abbrevationToNumber[abbr]

        except Exception as e:
            print(f"market capitalization of company {company} not available within API!")
            traceback.print_exc()

    def get_amount_shares(self, company: str):
        try:
            from requests_html import HTMLSession
            session = HTMLSession()
            response = session.get("https://finance.yahoo.com/quote/AAPL")

            share_value = response.html.find('[class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"]', first=True).text

            amount_shares = self.get_market_capitalization(company)/share_value

            return amount_shares

        except Exception as e:
            print(f"amount of shares of company {company} not available within API!")
            traceback.print_exc()

    def get_stock_chart(self, company: str):
        try:
            interval = '1wk'
            range = '5y'

            session = HTMLSession()
            response = session.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{company}'
                                   f'?region=US&interval={interval}&range={range}')
            response = json.loads(response.text)

            timestamps = response["chart"]["result"][0]["timestamp"]
            indicators = response["chart"]["result"][0]["indicators"]
            closing_prices = indicators["adjclose"][0]["adjclose"]

            chart_values = [{"x": datetime.fromtimestamp(timestamp), "y": price}
                            for timestamp, price in zip(timestamps, closing_prices)]

            # buffer = BytesIO()
            # plt.plot(closing_prices)
            # plt.savefig(buffer)
            # image = Image.open(buffer)

            return chart_values

        except:
            print(f"stock chart of company {company} not available within API!")
            traceback.print_exc()



    # TODO Other values?
