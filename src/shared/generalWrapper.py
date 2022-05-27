from bson.json_util import dumps
from src.shared.generalHelper import GeneralHelper

class GeneralWrapper:
    @staticmethod
    def successResult(data):
        return dumps(data), 200, {'Content-Type':'application/json'}

    @staticmethod
    def errorResult(code, message):
        data = {
            "code" : code,
            "message" : message
        }
        return dumps(data), GeneralHelper.getHttpStatusCode(code=code), {'Content-Type':'application/json'}