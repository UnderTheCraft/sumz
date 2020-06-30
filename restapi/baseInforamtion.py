from restapi.baseMethod import BaseMethod


class BaseInformation:
    """ Speichert Informationen zu bestimmten Verfahren zur Berechnung des Unternehmenswertes:
    In der Implementierung wird eine Erzeugung einer Instanz zur Verfügung gestellt """

    def __init__(self, method_name: object, method_description: object, method_class: BaseMethod):
        self.__method_name__ = method_name
        self.__method_description__ = method_description
        self.__method_class__ = method_class

    def dictDescription(self):
        description = {"method": self.__method_name__, "description": self.__method_description__}
        return description

    def getInstance(self):
        print(f"Initializing instance of {self.__method_name__} Class")
        return self.__method_class__

    def getMethodsElement(self):
        methods_element = {self.__method_name__:self}
        return methods_element
