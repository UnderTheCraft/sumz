from restapi.APV import APV


class APVInformation:

    def __init__(self):
        self.method_name = "APV"
        self.method_description = "Adjustet Present Value"

    def __repr__(self):
        repr = {"method": self.method_name, "description": self.method_description}
        return repr

    def getInstance(self):

        return APV().__class__