from flask import Flask, jsonify, make_response, render_template
from flask_api import status


def appFactory():
    app = Flask(__name__)
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
def companyCashFlows(company):
    if "adidas".__eq__(company.casefold()):
        response = jsonify(
            company=company,
            startingDate="01.01.2008",
            freeCashFlows=[22, 55, 64, 97, 87, 155, 99, 124, 136]
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
