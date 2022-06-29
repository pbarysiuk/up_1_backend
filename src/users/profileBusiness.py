
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.jwt import Jwt
import traceback
from src.shared.database import Database
from src.users.dataAccess import UsersDataAccess
from src.shared.passwordHelper import PasswordHelper
from src.users.wrapper import UsersWrapper


class ProfileBusiness:
    @staticmethod
    def changePassword(token, oldPassword, newPassword):
        try:
            payload = Jwt.checkAccessToken(token=token)
            GeneralHelper.checkString(oldPassword, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(newPassword, ResponseCodes.emptyOrInvalidPassword)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = UsersDataAccess.getById(db, userId, includePassword=True)
            PasswordHelper.checkPassword(existedUser["password"], oldPassword, ResponseCodes.oldPasswordNotMatch)
            UsersDataAccess.updatePassword(db, existedUser['_id'], PasswordHelper.hash(newPassword))
            return GeneralWrapper.successResult(UsersWrapper.profileResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def getProfile(token):
        try:
            payload = Jwt.checkAccessToken(token=token)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = UsersDataAccess.getById(db, userId)
            return GeneralWrapper.successResult(UsersWrapper.profileResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def updateProfile(token, email, name, image):
        try:
            payload = Jwt.checkAccessToken(token=token)
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            userId = GeneralHelper.getObjectId(payload["id"])
            existedUser = UsersDataAccess.getById(db, userId)
            UsersDataAccess.checkUniqueEmail(db, email, userId)
            UsersDataAccess.update(db, userId, name, email, existedUser['role'], image)
            existedUser = UsersDataAccess.getById(db, userId)
            return GeneralWrapper.successResult(UsersWrapper.profileResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)