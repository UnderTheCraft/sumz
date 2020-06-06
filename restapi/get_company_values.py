import pandas as pd
import json

# get cash flows of companies
def get_cash_flows(company: str):

    base_dir = "https://cloud-cube-eu.s3.amazonaws.com/mm6r5v7viahe/public"

    # Get from local files
    try:
        path = f"{base_dir}/{company.casefold()}.csv"
        print(path)
        df = pd.read_csv(path)
        return json.loads(df.to_json(orient='records'))
    except FileNotFoundError as e:
        print(e)
        print("company not found locally")

    # Get from an API
    try:
      # TODO request api or
      print("todo")
    except Exception:
        print("company not available within API")

    raise NotImplementedError("company not available locally and within API")

# get beta factor


# get "marktrisikoprämie"


# TODO Other values?