from src.shared.database import Database
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.xdl.dataAccess import XdlDataAccess
import traceback

class XdlBusiness:
    @staticmethod
    def add(drugs, filePath):
        try:
            GeneralHelper.checkString(filePath, ResponseCodes.emptyXdlFilePath)
            GeneralHelper.checkArray(drugs, ResponseCodes.emptyXdlName)
            for drug in drugs:
                GeneralHelper.checkString(drug['name'], ResponseCodes.emptyXdlName)
                GeneralHelper.checkString(drug['xml'], ResponseCodes.emptyXdlXml)
                GeneralHelper.checkString(drug['text'], ResponseCodes.emptyXdlText)
            dbConnection = Database()
            db = dbConnection.db
            XdlDataAccess.add(db, filePath, drugs)
            return GeneralWrapper.successResult({})
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def getList(query, pageSize, pageNumber):
        try:
            GeneralHelper.checkInteger(pageNumber, ResponseCodes.invalidPageNumber, allowSmallerThanZero=False)
            GeneralHelper.checkInteger(pageSize, ResponseCodes.invalidPageSize, allowSmallerThanZero=False)
            dbConnection = Database()
            db = dbConnection.db
            result = XdlDataAccess.getList(db, query, pageNumber, pageSize)
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def getDetails(id, allowRejected = True):
        try:
            GeneralHelper.checkString(id, ResponseCodes.xdlNotFound)
            dbConnection = Database()
            db = dbConnection.db
            result = XdlDataAccess.getDetails(db, id)
            if not (allowRejected) and (result['rejectedAt'] is not None):
                raise BusinessException(ResponseCodes.xdlNotFound)
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def changeStatus(id, status):
        try:
            GeneralHelper.checkString(id, ResponseCodes.xdlNotFound)
            approve = False
            if status == 1 or status == '1' or status == True:
                approve = True
            dbConnection = Database()
            db = dbConnection.db
            existedXdl = XdlDataAccess.getById(db, id)
            if not ((approve and existedXdl['approvedAt'] is not None) or (not approve and existedXdl['rejectedAt'] is not None)):
                XdlDataAccess.changeStatus(db, existedXdl, approve)
            return GeneralWrapper.successResult({})
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def search(query, pageSize, pageNumber):
        try:
            GeneralHelper.checkString(query, ResponseCodes.emptyXdlSearchQuery)
            GeneralHelper.checkInteger(pageNumber, ResponseCodes.invalidPageNumber, allowSmallerThanZero=False)
            GeneralHelper.checkInteger(pageSize, ResponseCodes.invalidPageSize, allowSmallerThanZero=False)
            dbConnection = Database()
            db = dbConnection.db
            result = XdlDataAccess.search(db, query, pageNumber, pageSize)
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)


    


