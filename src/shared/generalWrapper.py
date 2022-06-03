from bson.json_util import dumps
from src.shared.generalHelper import GeneralHelper

class GeneralWrapper:
    @staticmethod
    def successResult(data):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": dumps(data)
        }

    @staticmethod
    def generalErrorResult(e):
        result = {
            "message" : "An error occured",
            "exceptionType" : type(e),
            "exceptionMessage" : str(e),
            "exceptionArgs" : e.args
        }
        return {
            "isBase64Encoded": False,
            "statusCode": 500,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": dumps(result)
        }

    @staticmethod
    def errorResult(code, message):
        data = {
            "code" : code,
            "message" : message
        }
        return dumps(data), GeneralHelper.getHttpStatusCode(code=code), {'Content-Type':'application/json'}