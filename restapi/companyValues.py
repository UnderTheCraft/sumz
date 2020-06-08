from requests_html import HTMLSession
import pandas as pd
import traceback
from restapi.companyInfo import CompanyInfo

# TODO Import not used!
from dateutil.parser import parse

companies = CompanyInfo()

# get cash flows of companies
def get_cash_flows(company: str):

    local_companies = companies.get_local_companies()
    api_companies = companies.get_api_companies()

    if company.casefold() in local_companies:
        return get_from_local(company)
    elif company in api_companies:
        return get_from_api(company)
    else:
        try:
            cash_flows = get_from_api(company)
            return cash_flows
        except Exception as e:
            traceback.print_exc()
            raise NotImplementedError(f"Company {company} not available locally and within API")

# Get from local files
def get_from_local(company: str):
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
def get_from_api(company: str):
    try:
        print("get from API")
        abbrevationToNumber = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
        session = HTMLSession()

        # TODO hier könnte ne tryExcept hin, falls z.b. keine Verbindung aufgebaut werden kann
        response = session.get('https://ycharts.com/companies/' + company + '/free_cash_flow')

        print(f"The headers of the requests are:\n{response.headers}")

        rawDates = response.html.find(".histDataTable", first=True).find(".col1")
        rawFCFs = response.html.find(".histDataTable", first=True).find(".col2")
        currency = response.html.find("#securityQuote", first=True).find(".info")[1].text

        FCFs = []

        for i in range(1, len(rawDates)):
            parsedDate = rawDates[i].text
            parsedFCF = int(float(rawFCFs[i].text[:-1]) * 10 ** abbrevationToNumber[rawFCFs[i].text[-1]])

            FCFs.append([parsedDate, parsedFCF])

        result_df = pd.DataFrame(FCFs[0:16], columns=['Date', 'FCF'])
        result_json = result_df.to_dict(orient='records')
        result_json.append({"currency": currency})
        return result_json

    except Exception as e:
        print(f"company not available within API!")
        traceback.print_exc()

# ---------------------------------------------------------------------------------------------------------------------


# get beta factor


# get "marktrisikoprämie"


# TODO Other values?