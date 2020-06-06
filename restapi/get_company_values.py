from requests_html import HTMLSession
import pandas as pd
from dateutil.parser import parse

# get cash flows of companies
def get_cash_flows(company: str):

    #base_dir = "https://cloud-cube-eu.s3.amazonaws.com/mm6r5v7viahe/public"

    # Get from local files
    #try:
     #   path = f"{base_dir}/{company.casefold()}.csv"
      #  print(path)
       # df = pd.read_csv(path)
        #return df.to_json(orient='records')
    #except FileNotFoundError as e:
     #   print(e)
      #  print("company not found locally")


    # Get from an API
    try:
        abbrevationToNumber = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
        session = HTMLSession()
        response = session.get('https://ycharts.com/companies/' + company + '/free_cash_flow')
        rawDates = response.html.find(".histDataTable", first=True).find(".col1")
        rawFCFs = response.html.find(".histDataTable", first=True).find(".col2")

        FCFs = []

        for i in range(1, len(rawDates)):
            parsedDate = parse(rawDates[i].text)
            parsedFCF = int(float(rawFCFs[i].text[:-1]) * 10 ** abbrevationToNumber[rawFCFs[i].text[-1]])

            FCFs.append([parsedDate, parsedFCF])

        return pd.DataFrame(FCFs[0:16], columns=['Date', 'FCF']).to_json(orient='records')
    except Exception:
        print("company not available within API")

    raise NotImplementedError("company not available locally and within API")

# get beta factor


# get "marktrisikoprämie"


# TODO Other values?