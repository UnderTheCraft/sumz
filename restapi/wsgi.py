from flask import Flask, jsonify, make_response
from flask_api import status

application = Flask(__name__)


@application.route("/")
def index():
    return "This is the backend of sumz!"


@application.route("/echo/<string:message>")
def index(message):
    return f"This is your echo\n {message}"


@application.route("/getCashFlows/<company>")
def index(company):
    if "adidas".__eq__(company.casefold()):
        response = jsonify(
            company=company,
            startingDate="01.01.2008",
            freeCashFlows=[22,55,64,97,87,155,99,124,136]
        )
    elif "allianz".__eq__(company.casefold()):
        response = jsonify(
            company=company,
            startingDate="01.01.2012",
            freeCashFlows=[42, 75, 61, 87, 97, 125, 110, 124, 136]
        )
    elif "sap".__eq__(company.casefold()):
        response = jsonify(
            company=company,
            startingDate="01.01.2014",
            freeCashFlows=[24, 68, 100]
        )
    # TODO: Add companies
    else:
        return make_response(jsonify(), status.HTTP_404_NOT_FOUND)

    return make_response(response, status.HTTP_200_OK)
