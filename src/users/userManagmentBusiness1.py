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
from src.shared.passwordHelper import PasswordHelper
from src.users.wrapper import UsersWrapper
from src.users.usersDataAccess import UsersDataAccess
from src.users.apiKeysDataAccess import ApiKeysDataAccess
from os import environ

class UserManagmentBusiness:
    @staticmethod
    def __checkRole(role):
        if not (role in Jwt.roles):
            raise BusinessException(ResponseCodes.emptyOrInvalidRole)

    @staticmethod
    def insertDefaultUser():
        dbConnection = (Database())
        db = dbConnection.db
        userName = "admin"
        email = "admin@prepaire.com"
        password = "Prepaire@dmin"
        role = "admin"
        apiKey = ApiKeysDataAccess.create("defaultUser", GeneralHelper.generateGUID(), environ.get("USAGE_PLAN_ID"))
        UsersDataAccess.addDefault(db, userName, email, PasswordHelper.hash(password), role, None, apiKey['id'], apiKey['value'])
        return "done!"

    @staticmethod
    def addUser(token, name, email, role, image):
        try:
            tokenPayload = Jwt.checkAccessToken(token, [Jwt.adminRole])
            adminId = tokenPayload['id']
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
            insertResult = UsersDataAccess.add(db, name, email, PasswordHelper.hash(password), role, image, verificatioCode, None, adminId)
            Email.sendCreateUserEmail(email, password)
            existedUser = UsersDataAccess.getById(db, insertResult.inserted_id)
            return GeneralWrapper.successResult(UsersWrapper.detailsResult(existedUser))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)