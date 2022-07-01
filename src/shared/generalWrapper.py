from bson.json_util import dumps
from src.shared.generalHelper import GeneralHelper
from os import environ 

class GeneralWrapper:
    @staticmethod
    def successResult(data):
        if data is None:
            data = {
                'code' : 200,
                "message" : 'success'
            }
        if environ.get('LOCAL'):
            return dumps(data, default=vars), 200, {'Content-Type':'application/json'}
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": dumps(data)
        }

    @staticmethod
    def generalErrorResult(e):
        result = {
            'code' : 500,
            "message" : "An error occured",
            "exceptionMessage" : str(e)
        }
        if environ.get('LOCAL'):
            return dumps(result, default=vars), 500, {'Content-Type':'application/json'}
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
        if environ.get('LOCAL'):
            return dumps(data, default=vars), GeneralHelper.getHttpStatusCode(code=code), {'Content-Type':'application/json'}
        return {
            "isBase64Encoded": False,
            "statusCode": GeneralHelper.getHttpStatusCode(code=code),
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": dumps(data)
        }
