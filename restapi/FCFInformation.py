from restapi.FCF import FCF
from restapi.baseInforamtion import BaseInformation


class FCFInformation(BaseInformation):

    def __init__(self):
        super().__init__(method_name="FCF", method_description="Free Cash Flow Method", methodClass=FCF)
