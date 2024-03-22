from abc import ABC, abstractmethod

from eccovjson.Coverage import Coverage
from eccovjson.CoverageCollection import CoverageCollection


class Encoder(ABC):
    def __init__(self, type, domaintype):
        self.covjson = {}

        self.type = type
        self.parameters = []
        self.covjson["type"] = self.type
        self.covjson["domainType"] = domaintype
        self.covjson["coverages"] = []
        self.covjson["parameters"] = {}
        self.covjson["referencing"] = []

        if type == "Coverage":
            self.coverage = Coverage(self.covjson)
        elif type == "CoverageCollection":
            self.coverage = CoverageCollection(self.covjson)
        else:
            raise TypeError("Type must be Coverage or CoverageCollection")

    def add_parameter(self, param):
        param = self.convert_param_id_to_param(param)
        if param == "T_2M" or param == "500011":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "2m Temperature",
                "unit": {"symbol": "K"},
                "observedProperty": {
                    "id": "T_2M",
                    "label": {"en": "2m Temperature"},
                },
            }
        elif param == "TOT_PREC" or param == "500041":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "Total Precipitation",
                "unit": {"symbol": "m"},
                "observedProperty": {
                    "id": "tp",
                    "label": {"en": "Total Precipitation"},
                },
            }
        elif param == "U_10M" or param == "500027":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "10 metre U wind component",
                "unit": {"symbol": "ms-1"},
                "observedProperty": {
                    "id": "U_10M",
                    "label": {"en": "10 metre U wind component"},
                },
            }
        elif param == "V_10M" or param == "500029":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "10 metre V wind component",
                "unit": {"symbol": "ms-1"},
                "observedProperty": {
                    "id": "V_10M",
                    "label": {"en": "10 metre V wind component"},
                },
            }
        elif param == "CLCT" or param == "500046":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "Total cloud cover",
                "unit": {"symbol": ""},
                "observedProperty": {
                    "id": "CLCT",
                    "label": {"en": "Total cloud cover"},
                },
            }
        elif param == "TD_2M" or param == "500017":
            self.covjson["parameters"][param] = {
                "type": "Parameter",
                "description": "2 metre dewpoint temperature",
                "unit": {"symbol": "K"},
                "observedProperty": {
                    "id": "TD_2M",
                    "label": {"en": "2 metre dewpoint temperature"},
                },
            }
        self.parameters.append(param)

    def add_reference(self, reference):
        self.covjson["referencing"].append(reference)

    def convert_param_id_to_param(self, paramid):
        try:
            param = int(paramid)
        except BaseException:
            return paramid
        if param == 500027:
            return "U_10M"
        elif param == 500029:
            return "V_10M"
        elif param == 500011:
            return "T_2M"
        elif param == 500041:
            return "TOT_PREC"
        elif param == 500046:
            return "CLCT"
        elif param == 500017:
            return "TD_2M"

    @abstractmethod
    def add_coverage(self, mars_metadata, coords, values):
        pass

    @abstractmethod
    def add_domain(self, coverage, domain):
        pass

    @abstractmethod
    def add_range(self, coverage, range):
        pass

    @abstractmethod
    def add_mars_metadata(self, coverage, metadata):
        pass

    @abstractmethod
    def from_xarray(self, dataset):
        pass

    @abstractmethod
    def from_polytope(self, result):
        pass
