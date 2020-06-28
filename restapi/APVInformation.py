from restapi.APV import APV
from restapi.baseInforamtion import BaseInformation


class APVInformation(BaseInformation):

    def __init__(self):
        super().__init__(method_name="APV", method_description="Adjusted Present Value", method_class=APV)
