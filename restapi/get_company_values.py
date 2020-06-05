import pandas as pd

# get cash flows of companies
def get_company_cash_flows(company: str):

    base_dir = "data/fcf"

    # Get from local files
    try:
        df = pd.read_csv(f"{base_dir}/{company}")
        return df.to_json(orient='records')
    except FileNotFoundError:
        print("company not found locally")

    # Get from an API
    try:
      # TODO request api or
      return []
    except Exception:
        print("company not available within API")

    raise NotImplementedError("company not available locally and within API")

# get beta factor


# get "marktrisikoprämie"


# TODO Other values?