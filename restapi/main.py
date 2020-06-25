from datetime import datetime
from flask import Flask, jsonify, make_response, request, send_file
from flask_cors import CORS
from flask_api import status
from flask_restx import Api, Resource

from restapi.APVInformation import APVInformation
from restapi.arimaForecast import ARIMAForecast
from restapi.companyInfo import CompanyInfo
from restapi.companyValues import CompanyValues
from restapi.marketValues import MarketValues

import pandas as pd
import numpy as np

flask_app = Flask(__name__)
print("Flask App created")
CORS(flask_app)
print("CORS added")
application = Api(app=flask_app,
                  title="SUMZ",
                  description="Das Backend der SUMZ Anwendung für Unternehmensbewertung")
print("RestX created")

companyInfo = CompanyInfo()
companyValues = CompanyValues()
marketValues = MarketValues()
# TODO Metodenliste auslagern
methods = {APVInformation().method_name: APVInformation()}

@application.route("/")
class MainClass(Resource):
    def get(self):
        return make_response("Hello World", status.HTTP_200_OK)

@application.route("/getCorporateValue/<string:company>/<string:method>")
class EnterpriseValueCalculation(Resource):
    def get(self, company: str, method: str):

        print("EnterpriseValueCalculation Started!")
        print(f"Using Company {company} and method {method}")

        last_date = request.args.get('last_date')
        if last_date is not None:
            last_date = datetime.strptime(last_date, "%d.%m.%Y").date()
        risk_free_interest_rate = request.args.get('risk_free_interest_rate')
        if risk_free_interest_rate is not None:
            risk_free_interest_rate = float(risk_free_interest_rate)
        market_risk_premium = request.args.get('market_risk_premium')
        if market_risk_premium is not None:
            market_risk_premium = float(market_risk_premium)

        enterpriseValueCalculator = methods[method].getInstance()(company=company, last_date=last_date,
                                                                  risk_free_interest_rate=risk_free_interest_rate,
                                                                  market_risk_premium=market_risk_premium)

        enterpriseValue = enterpriseValueCalculator.calculateEnterpriseValue()

        additionalInformation = enterpriseValueCalculator.getAdditionalValues(enterpriseValue, percentage_deviation=5)

        response = {"Enterprise Value": enterpriseValue, **additionalInformation}

        return make_response(response, status.HTTP_200_OK)

@application.route("/companies", methods=['GET'])
class Companies(Resource):
    def get(self):
        return companyInfo.get_all_companies()


@application.route("/methods", methods=['GET'])
class Methods(Resource):
    def get(self):
        print(methods)
        response = [method.dictDescription() for method in methods.values()]
        return response


@application.route("/getCashFlows/<string:company>", methods=['GET'])
class CashFlows(Resource):
    def get(self, company):
        try:
            company_cash_flows = companyValues.get_cash_flows(company.upper(),True)
            company_cash_flows.append({"company": company})
            response = make_response(jsonify(company_cash_flows), status.HTTP_200_OK)
            response.headers['content-type'] = 'application/json'
            print("returning response object")
            return response

        except NotImplementedError as e:
            return make_response(f"Das Unternehmen {company} ist nicht verfügbar {str(e)}",
                                 status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            print("Es ist ein schwerwiegender Fehler aufgetreten")
            print(e)
            return make_response(f"Die Anfrage für das Unternehmen {company} konnte nicht bearbeitet werden!",
                                 status.HTTP_500_INTERNAL_SERVER_ERROR)


@application.route("/getCashFlowForecast/<string:company>/prediction_length=<int:prediction_length>", methods=['GET'])
class CashFlowForecast(Resource):
    def get(self, company, prediction_length):
        dates, fcfs, currency = CompanyValues().get_cash_flows(company)
        fcfs = fcfs[0:20]
        fcfs.reverse()
        forecast = ARIMAForecast().make_forecast(fcfs, prediction_length)

        forecast_df = pd.DataFrame()
        forecast_df["fcf"] = forecast
        result = [{"company": company,
                   "prediction_length": prediction_length,
                   "forecast": forecast_df.to_dict(orient='records')}]
        response = make_response(jsonify(result), status.HTTP_200_OK)
        response.headers['content-type'] = 'application/json'
        return response


@application.route("/getDefaultExpertValues", methods=['GET'])
class DefaultExpertValues(Resource):
    def get(self):
        response = {"risk_free_interest": marketValues.get_risk_free_interest(),
                    "market_risk_premium": marketValues.get_market_risk_premium()}
        return make_response(response, status.HTTP_200_OK)


@application.route("/getBetaFactor/<string:company>", methods=['GET'])
class BetaFactor(Resource):
    def get(self, company):
        response = {"beta_factor": companyValues.get_beta_factor(company)}
        return make_response(response, status.HTTP_200_OK)


@application.route("/getAnnualLiabilities/<string:company>", methods=['GET'])
class YearlyLiabilities(Resource):
    def get(self, company):
        response = {"total_liabilities": companyValues.get_liabilities(company,False,True)}
        return make_response(response, status.HTTP_200_OK)


@application.route("/getAnnualCashFlows/<string:company>", methods=['GET'])
class AnnualFreeCashFlows(Resource):
    def get(self, company):
        response = {"free_cash_flows": companyValues.get_annual_cash_flow(company)}
        return make_response(response,status.HTTP_200_OK)

@application.route("/getQuarterlyLiabilities/<string:company>", methods=['GET'])
class QuarterlyLiabilities(Resource):
    def get(self, company):
        response = {"total_liabilities": companyValues.get_liabilities(company, True,True)}
        return make_response(response, status.HTTP_200_OK)


@application.route("/getMarketCapitalization/<string:company>", methods=["GET"])
class MarketCapitalization(Resource):
    def get(self, company):
        response = {"market_capitalization": companyValues.get_market_capitalization(company)}
        return make_response(response, status.HTTP_200_OK)

@application.route("/getMarketCapitalizationAndAmountShares/<string:company>", methods=["GET"])
class MarketCapitalization(Resource):
    def get(self, company):
        market_capitalization, amount_shares = companyValues.get_market_capitalization_and_amount_shares(company)
        response = {"market_capitalization": market_capitalization, "amount_shares": amount_shares}
        return make_response(response, status.HTTP_200_OK)

@application.route("/getStockChart/<string:company>", methods=['GET'])
class StockChart(Resource):
    def get(self, company):
        response = {"dataPoints": companyValues.get_stock_chart(company)}
        return make_response(response, status.HTTP_200_OK)
        # return make_response(chart_image, status.HTTP_200_OK)
