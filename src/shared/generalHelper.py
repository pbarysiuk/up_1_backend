from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
import re
from bson.objectid import ObjectId
import uuid
from random import randint

class GeneralHelper:
    
    @staticmethod
    def getObjectId(id):
        if id is None:
            return None
        if type(id) == ObjectId:
            return id
        return ObjectId(id)

    @staticmethod
    def checkId(id, errorCode):
        if id is None or type(id) != int or id <= 0:
            raise BusinessException(errorCode)
    
    @staticmethod
    def isValidString(string):
        if string is None or type(string) != str or len(string) <= 0:
            return False
        return True

    @staticmethod
    def checkString(string, errorCode):
        if not GeneralHelper.isValidString(string):
            raise BusinessException(errorCode)

    @staticmethod
    def checkArray(arr, errorCode):
        if arr is None or (type(arr) != list) or len(arr) <= 0:
            raise BusinessException(errorCode)
    
    @staticmethod
    def checkInteger(number, errorCode, allowSmallerThanZero = True):
        if number is None or type(number) != int:
            raise BusinessException(errorCode)
        if not (allowSmallerThanZero) and number < 0:
            raise BusinessException(errorCode)

    @staticmethod
    def checkEmailFormat(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(regex, email)):
            raise BusinessException(ResponseCodes.invalidEmailFormat)

    @staticmethod
    def getHttpStatusCode(code):
        if code == '200':
            return 200
        if code == '500':
            return 500
        if code >= '400-000' and code <= '400-999':
            return 400
        if code >= '401-000' and code <= '401-999':
            return 401
        if code >= '403-000' and code <= '403-999':
            return 403
        if code >= '404-000' and code <= '404-999':
            return 404
        if code >= '409-000' and code <= '409-999':
            return 409
        return 200

    @staticmethod
    def generateGUID():
        return str(uuid.uuid4())

    @staticmethod
    def generateCode():
        return str(randint(100000, 999999))

