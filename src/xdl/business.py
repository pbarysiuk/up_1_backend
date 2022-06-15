from src.shared.database import Database
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.xdl.dataAccess import XdlDataAccess
from src.xdl.wrapper import XdlWrapper
import traceback

class XdlBusiness:
    @staticmethod
    def add(drugs, filePath):
        try:
            GeneralHelper.checkString(filePath, ResponseCodes.emptyXdlFilePath)
            GeneralHelper.checkArray(drugs, ResponseCodes.badXdlRequest)
            acceptedDrugs = []
            for drug in drugs:
                if (GeneralHelper.isValidString(drug['name']) and GeneralHelper.isValidString(drug['xml']) and GeneralHelper.isValidString(drug['text'])):
                    acceptedDrugs.append(drug)
            dbConnection = Database()
            db = dbConnection.db
            XdlDataAccess.add(db, filePath, acceptedDrugs)
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
            count, items = XdlDataAccess.getList(db, query, pageNumber, pageSize)
            return GeneralWrapper.successResult(XdlWrapper.listResult(items, count))
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
            if not (allowRejected) and (result['status'] == XdlDataAccess.status['rejected']):
                raise BusinessException(ResponseCodes.xdlNotFound)
            return GeneralWrapper.successResult(XdlWrapper.detailsResult(result))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def changeStatus(id, status, name):
        try:
            GeneralHelper.checkString(id, ResponseCodes.xdlNotFound)
            approve = False
            if status == 1 or status == '1' or status == True:
                approve = True
            dbConnection = Database()
            db = dbConnection.db
            existedXdl = XdlDataAccess.getById(db, id)
            if (not GeneralHelper.isValidString(name)):
                name = existedXdl['name']
            XdlDataAccess.changeStatus(db, existedXdl, approve, name, None)
            #if not ((approve and existedXdl['status'] == XdlDataAccess.status['approved']) or (not approve and existedXdl['status'] == XdlDataAccess.status['rejected'])):
            #    XdlDataAccess.changeStatus(db, existedXdl, approve, None)
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
            count, items = XdlDataAccess.search(db, query, pageNumber, pageSize)
            return GeneralWrapper.successResult(XdlWrapper.searchResult(items, count))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)


    


