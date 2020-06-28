from restapi import baseMethod


class BaseInformation:

    def __init__(self, method_name: object, method_description: object, methodClass: object) -> object:
        self.__method_name__ = method_name
        self.__method_description__ = method_description
        self.__methodClass__ = methodClass

    def dictDescription(self):
        description = {"method": self.__method_name__, "description": self.__method_description__}
        return description

    def getInstance(self):
        print(f"Initializing instance of {self.__method_name__} Class")
        return self.__methodClass__

    def getMethodsElement(self):
        methodsElement = {self.__method_name__:self}
        return methodsElement
