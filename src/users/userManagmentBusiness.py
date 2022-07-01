from src.shared.database import Database
from src.shared.generalHelper import GeneralHelper
from datetime import timezone,datetime
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import  ResponseCodes
from src.shared.exceptions.responseMessages import ResponseMessages
from src.shared.jwt import Jwt
from src.shared.generalWrapper import GeneralWrapper
import traceback
from src.shared.emails import Email
from src.users.dataAccess import UsersDataAccess
from src.shared.passwordHelper import PasswordHelper
from src.users.wrapper import UsersWrapper

class UserManagmentBusiness:
    @staticmethod
    def __checkRole(role):
        if not (role in Jwt.roles):
            raise BusinessException(ResponseCodes.emptyOrInvalidRole)

    @staticmethod
    def insertDefaultUser():
        dbConnection = (Database())
        db = dbConnection.db
        count  = UsersDataAccess.getCountOfNotDeletedUsers(db)
        if count > 0:
            return 'Already found admin users'
        UsersDataAccess.insertUser(db, "admin", "admin@prepaire.com", PasswordHelper.hash("Prepaire@dmin"), "admin", None, None, True)
        return "done!"

    @staticmethod
    def addUser(token, name, email, role, image):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(role, ResponseCodes.emptyOrInvalidRole)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            UserManagmentBusiness.__checkRole(role.lower())
            dbConnection = (Database())
            db = dbConnection.db
            UsersDataAccess.checkUniqueEmail(db, email)
            password = GeneralHelper.generateGUID()
            verificatioCode = GeneralHelper.generateCode()
            insertResult = UsersDataAccess.insertUser(db, name, email, PasswordHelper.hash(password), role.lower(), image, verificatioCode)
            Email.sendCreateUserEmail(email, password)
            existedUser = UsersDataAccess.getById(db, insertResult.inserted_id)
            return GeneralWrapper.successResult(UsersWrapper.detailsResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    
    @staticmethod
    def updateUser(token, userId, name, email, role, image):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(role, ResponseCodes.emptyOrInvalidRole)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            UserManagmentBusiness.__checkRole(role.lower())
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getById(db, userId)
            UsersDataAccess.checkUniqueEmail(db, email, userId)
            UsersDataAccess.update(db, existedUser['_id'], name, email, role, image)
            existedUser = UsersDataAccess.getById(db, userId)
            return GeneralWrapper.successResult(UsersWrapper.detailsResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def deleteUser(token, userId):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getById(db, userId)
            UsersDataAccess.delete(db, userId)
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def getUser(token, userId):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getById(db, userId)
            return GeneralWrapper.successResult(UsersWrapper.detailsResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def getUsersList(token, criteria, pageNumber, pageSize=10):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            GeneralHelper.checkInteger(pageNumber, ResponseCodes.invalidPageNumber, allowSmallerThanZero=False)
            GeneralHelper.checkInteger(pageSize, ResponseCodes.invalidPageSize, allowSmallerThanZero=False)
            dbConnection = (Database())
            db = dbConnection.db
            count, items = UsersDataAccess.getList(db, criteria, pageNumber, pageSize)
            return GeneralWrapper.successResult(UsersWrapper.listResult(items, count))      
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)