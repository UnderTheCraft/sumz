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


@application.route("/echo/<string:message>")
def test(message):
    return f"This is your echo\n {message}"


@application.route("/getCashFlows/<company>")
def companyCashFlows(company: str):
    from . import get_company_values

    try:
        company_cash_flows = get_company_values.get_cash_flows(company)
        company_cash_flows.append({"company": company.casefold()})

        cf_response = Response(company_cash_flows)
        response = make_response(cf_response, status.HTTP_200_OK)
        response.headers['content-type'] = 'application/json'
        return response

    except NotImplementedError as e:
        return make_response(f"Das Unternehmen {company} ist nicht verfügbar {str(e)}", status.HTTP_404_NOT_FOUND)


@application.route("/getCashFlowForecast/<company>&prediction_length=<prediction_length>")
def forecastCashFlow(company: str, prediction_length: int):

    return make_response(f"Company {company} and prediction length {prediction_length}", status.HTTP_200_OK)