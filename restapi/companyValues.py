from requests_html import HTMLSession
import pandas as pd
import traceback
from restapi.companyInfo import CompanyInfo
from dateutil import parser

class CompanyValues:

    def __init__(self):
        self.__companies = CompanyInfo()

    # get cash flows of companies
    def get_cash_flows_json(self, company: str):
        local_companies = self.__companies.get_local_companies()
        api_companies = self.__companies.get_api_companies()

        if company.casefold() in local_companies:
            return self.get_from_local(company)
        elif company in api_companies:
            return self.get_from_api(company)
        else:
            try:
                cash_flows = self.get_from_api(company)
                return cash_flows
            except Exception as e:
                traceback.print_exc()
                raise NotImplementedError(f"Company {company} not available locally and within API")

    # Get from local files
    def get_from_local(self, company: str):
        base_dir = "https://cloud-cube-eu.s3.amazonaws.com/mm6r5v7viahe/public"

        try:
            path = f"{base_dir}/{company.casefold()}.csv"
            result_df = pd.read_csv(path, sep=";")
            result_json = result_df.to_dict(orient='records')
            result_json.append({"currency": "EUR"})
            return result_json

        except FileNotFoundError as e:
            print("company not found locally")
            traceback.print_exc()

    # Get from an API
    def get_from_api(self, company: str):
        print("get from API")

        dates, fcfs, currency = self.get_cash_flows_array(company)

        result_df = pd.DataFrame()
        result_df["date"] = dates
        result_df["FCF"] = fcfs

        result_json = [{"Free Cash Flows": result_df.to_dict(orient='records')}, {"currency": currency}]

        return result_json


    def get_cash_flows_array(self, company):

        try:
            abbrevationToNumber = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
            session = HTMLSession()

            # TODO hier könnte ne tryExcept hin, falls z.b. keine Verbindung aufgebaut werden kann
            response = session.get(f'https://ycharts.com/companies/{company}/free_cash_flow')

            print(f"The headers of the requests are:\n{response.headers}")

            raw_dates = response.html.find(".histDataTable", first=True).find(".col1")[1:]
            raw_fcfs = response.html.find(".histDataTable", first=True).find(".col2")[1:]
            currency = response.html.find("#securityQuote", first=True).find(".info")[1].text

            dates = [parser.parse(rawDate.text) for rawDate in raw_dates]
            fcfs = [int(float(rawFCF.text[:-1]) * 10 ** abbrevationToNumber[rawFCF.text[-1]]) for rawFCF in raw_fcfs]

            return dates,fcfs,currency

        except Exception as e:
            print(f"company not available within API!")
            traceback.print_exc()

    # ---------------------------------------------------------------------------------------------------------------------


    # get beta factor
    def get_beta_factor(self, company: str):
        try:
            session = HTMLSession()
            response = session.get(f'https://finance.yahoo.com/quote/{company}')
            beta_factor = response.html.find("[data-test='BETA_5Y-value']", first=True).text
            return beta_factor

        except Exception as e:
            print(f"company not available within API!")
            traceback.print_exc()

    # get Liablilities (Fremdkapital)
    def get_liabilities(self, company: str):
        try:
            session = HTMLSession()
            response = session.get(f'https://finance.yahoo.com/quote/{company}/balance-sheet')

            ''' HTML Aufbau
            find: <div class="Pos(r)">
                <div (Total Assets...)>
                <div (Total Liabilities...)>
                    <div (irgendwas bzw. erster eintrag)>
                        <div (beschreibung reihe)>
                        <div (erster Eintrag reihe -> jüngste verfügbare Zahl)>
                            <span (mit der benötigten Zahl)>
            '''
            root_table = response.html.find(".Pos\(r\)", first=True)
            total_liabilities = root_table.find("div")[1].find("div")[0]
            row_liabilities = total_liabilities.find("div")[1]
            liabilities = row_liabilities.find("span", first=True).text
            return liabilities

        except Exception as e:
            print(f"company not available within API!")
            traceback.print_exc()

    # TODO Other values?
