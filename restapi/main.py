from flask import Flask, jsonify, make_response, render_template, Response
from flask_cors import CORS
from flask_api import status


def appFactory():
    app = Flask(__name__)
    CORS(app)
    return app


application = appFactory()


@application.route("/")
def starting():
    # TODO: add an overview of available APIs
    return render_template('index.html')

@application.route("/companies")
def get_companies():
    from . import companyInfo
    return companyInfo.get_all_companies()

@application.route("/methods")
def get_methods():
    return {"methods": {"name": "APV", "description": "Adjusted Present Value"}}


@application.route("/getCashFlows/<company>")
def get_company_cash_flows(company: str):
    from . import companyValues
    import json

    try:
        company_cash_flows = companyValues.get_cash_flows(company)
        company_cash_flows.append({"company": company.casefold()})

        #cf_response = Response(json.dump(company_cash_flows))
        #print("created cf_response object")

        response = make_response(jsonify(company_cash_flows), status.HTTP_200_OK)
        response.headers['content-type'] = 'application/json'
        print("returning response object")
        return response

    except NotImplementedError as e:
        return make_response(f"Das Unternehmen {company} ist nicht verfügbar {str(e)}", status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print("Es ist ein schwerwiegender Fehler aufgetreten")
        print(e)

    return make_response(f"Die Anfrage für das Unternehmen {company} konnte nicht bearbeitet werden!")


@application.route("/getCashFlowForecast/<company>&prediction_length=<prediction_length>")
def get_forecast_cash_flows(company: str, prediction_length: int):

    return make_response(f"Company {company} and prediction length {prediction_length}", status.HTTP_200_OK)