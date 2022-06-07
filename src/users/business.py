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

class BusinessUsers:
    @staticmethod
    def __insertUser(db, name, email, password, role):
        user = {
            "name" : name,
            "email" : email,
            "password" : password,
            "role" : role,
            "created_at" : datetime.now(tz=timezone.utc),
            "updated_at" : None,
            "deleted_at" : None
        }
        return db.users.insert_one(user)

    @staticmethod
    def __checkRole(role):
        if not (role in Jwt.roles):
            raise BusinessException(ResponseCodes.emptyOrInvalidRole)

    @staticmethod
    def __checkUniqueEmail(db, email, id = None):
        query = {
            "email" : email,
            'deleted_at': None,
            "_id" : {
                '$ne' : GeneralHelper.getObjectId(id=id)
            }
        }
        count = db.users.count_documents(query)
        if count > 0:
            raise BusinessException(ResponseCodes.duplicateEmail)

    @staticmethod
    def __getById(db, id, throwExceptionIfNotFound = True, includePassword = False):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'deleted_at': None
        }
        projection = {
            "name" : 1,
            "email" : 1,
            "role" : 1,
            "created_at" : 1,
            "updated_at" : 1
        }
        if includePassword:
            projection["password"] = 1
        existedUser = db.users.find_one(query, projection)
        if existedUser is None:
            if throwExceptionIfNotFound:
                raise BusinessException(ResponseCodes.userNotFound)
            return None
        return existedUser



    @staticmethod
    def insertDefaultUser():
        dbConnection = (Database())
        db = dbConnection.db
        query = {
            'deleted_at': None,
            'role' : 'admin'
        }
        count = db.users.count_documents(query)
        if count > 0:
            return 'Already found admin users'
        BusinessUsers.__insertUser(db, "admin", "admin@prepaire.com", GeneralHelper.hash("Prepaire@dmin"), "admin")
        return "done!"

    @staticmethod
    def changePassword(token, oldPassword, newPassword):
        try:
            payload = Jwt.checkAccessToken(token=token)
            GeneralHelper.checkString(oldPassword, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(newPassword, ResponseCodes.emptyOrInvalidPassword)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = BusinessUsers.__getById(db, userId, includePassword=True)
            if GeneralHelper.hash(oldPassword) != existedUser["password"]:
                raise BusinessException(ResponseCodes.oldPasswordNotMatch)
            db.users.update_one({"_id" : userId}, {"$set": {"password" : GeneralHelper.hash(newPassword)}})
            existedUser = BusinessUsers.__getById(db, userId)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def getProfile(token):
        try:
            payload = Jwt.checkAccessToken(token=token)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = BusinessUsers.__getById(db, userId)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def updateProfile(token, email, name):
        try:
            payload = Jwt.checkAccessToken(token=token)
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = BusinessUsers.__getById(db, userId, includePassword=False)
            BusinessUsers.__checkUniqueEmail(db, email, userId)
            setQuery={
                "name" : name,
                "email" : email,
                "updated_at" : datetime.now(tz=timezone.utc)
            }
            db.users.update_one({"_id" : userId}, {"$set": setQuery})
            existedUser = BusinessUsers.__getById(db, userId)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def addUser(token, name, email, password, role):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(role, ResponseCodes.emptyOrInvalidRole)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            BusinessUsers.__checkRole(role.lower())
            dbConnection = (Database())
            db = dbConnection.db
            BusinessUsers.__checkUniqueEmail(db, email)
            insertResult = BusinessUsers.__insertUser(db, name, email, GeneralHelper.hash(password), role.lower())
            Email.sendCreateUserEmail(email, password)
            existedUser = BusinessUsers.__getById(db, insertResult.inserted_id)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def updateUser(token, userId, name, email, role):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(role, ResponseCodes.emptyOrInvalidRole)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            BusinessUsers.__checkRole(role.lower())
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = BusinessUsers.__getById(db, userId)
            BusinessUsers.__checkUniqueEmail(db, email, userId)
            setQuery={
                "name" : name,
                "email" : email,
                "role" : role,
                "updated_at" : datetime.now(tz=timezone.utc)
            }
            db.users.update_one({"_id" : userId}, {"$set": setQuery})
            existedUser = BusinessUsers.__getById(db, userId)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def deleteUser(token, userId):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = BusinessUsers.__getById(db, userId)
            setQuery={
                "deleted_at" : datetime.now(tz=timezone.utc)
            }
            db.users.update_one({"_id" : userId}, {"$set": setQuery})
            return GeneralWrapper.successResult({})
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def getUser(token, userId):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            userId = GeneralHelper.getObjectId(userId)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = BusinessUsers.__getById(db, userId)
            return GeneralWrapper.successResult(existedUser)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def getUsersList(token, criteria, page, pageSize=10):
        try:
            Jwt.checkAccessToken(token, [Jwt.adminRole])
            GeneralHelper.checkInteger(page, ResponseCodes.invalidPageNumber, allowSmallerThanZero=False)
            GeneralHelper.checkInteger(pageSize, ResponseCodes.invalidPageSize, allowSmallerThanZero=False)
            if criteria is None:
                criteria = ""
            projection = {
                "name" : 1,
                "email" : 1,
                "role" : 1,
                "created_at" : 1,
                "updated_at" : 1
            }
            orQuery = {
                "$or" : [
                    {
                        "name" : {
                            "$regex": ".*{}.*".format(criteria),
                            "$options": "i"
                        }
                    },
                    {
                        "email" : {
                            "$regex": ".*{}.*".format(criteria),
                            "$options": "i"
                        }
                    }
                ]
            }
            query = {
                "$and" : [
                    orQuery,
                    {
                        "deleted_at" : None
                    }
                ]
            }
            dbConnection = (Database())
            db = dbConnection.db
            users = db.users.find(query, projection).skip((page-1) * pageSize).limit(pageSize)
            count = db.users.count_documents(query)
            result = {
                "count" : count,
                "items" : users
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])