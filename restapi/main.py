from flask import Flask, jsonify, make_response, render_template, Response
from flask_cors import CORS
from flask_api import status
from flask_restx import Api, Resource

from restapi.arimaForecast import ARIMAForecast
from restapi.companyInfo import CompanyInfo
from restapi.companyValues import CompanyValues

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

@application.route("/")
class MainClass(Resource):
    def get(self):
        return make_response("Hello World", status.HTTP_200_OK)

@application.route("/companies", methods=['GET'])
class Companies(Resource):
    def get(self):
        return companyInfo.get_all_companies()


@application.route("/methods", methods=['GET'])
class Methods(Resource):
    def get(self):
        return {"methods": {"name": "APV", "description": "Adjusted Present Value"}}


@application.route("/getCashFlows/<string:company>", methods=['GET'])
class CashFlows(Resource):
    def get(self, company):
        try:
            company_cash_flows = companyValues.get_cash_flows_json(company)
            company_cash_flows.append({"company": company.casefold()})

            # cf_response = Response(json.dump(company_cash_flows))
            # print("created cf_response object")

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

@application.route("/getCashFlowForecast/<string:company>&prediction_length=<int:prediction_length>", methods=['GET'])
class CashFlowForecast(Resource):
    def get(self, company, prediction_length):

        dates, fcfs, currency = CompanyValues().get_cash_flows_array(company)

        forecast = ARIMAForecast.make_forecast(fcfs[0:16], prediction_length)

        forecast_df = pd.DataFrame()
        forecast_df["fcf"] = forecast
        response = []
        response.append({"compnay":company,"prediction_length":prediction_length,"forecast":forecast_df.to_dict(orient='records')})
        response = make_response(jsonify(response),status.HTTP_200_OK)
        response.headers['content-type'] = 'application/json'

        return response
