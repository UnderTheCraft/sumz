from restapi.baseMethod import BaseMethod
from math import floor

class FCF(BaseMethod):

    def __init__(self):
        pass

    def calculateEnterpriseValue(self):
        """ Hauptmethode für die Berechnung des Unternehmenswertes """

        enterprise_value = self.calculatePresentValueOfCashFlow() - self.getDebt()

        return floor(enterprise_value)