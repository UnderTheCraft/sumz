from flask import Flask, jsonify, make_response, render_template
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
        response = jsonify(
            company=company,
            cashflows=company_cash_flows
        )
        return make_response(response, status.HTTP_200_OK)

    except NotImplementedError:
        return make_response(jsonify(), status.HTTP_404_NOT_FOUND)


@application.route("/getCashFlowForecast/<company>&prediction_length=<prediction_length>")
def forecastCashFlow(company: str, prediction_length: int):

    return make_response(f"Company {company} and prediction length {prediction_length}", status.HTTP_200_OK)