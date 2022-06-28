from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.exceptions.responseMessages import ResponseMessages
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.jwt import Jwt
import traceback
from datetime import timezone,datetime
from src.shared.emails import Email
from src.shared.database import Database
from src.users.dataAccess import UsersDataAccess
from src.shared.passwordHelper import PasswordHelper
from src.users.wrapper import UsersWrapper

class BusinessAuth:
    @staticmethod
    def login(email, password):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email, False, True)
            if existedUser is None:
                raise BusinessException(ResponseCodes.wrongEmailOrPassword) 
            PasswordHelper.checkPassword(existedUser['password'], password, ResponseCodes.wrongEmailOrPassword)
            if existedUser['verifiedAt'] is None:
                Email.sendVerificationEmail(existedUser['email'], existedUser['verificationCode'])
                raise BusinessException(ResponseCodes.notVerifiedUser)    
            accessToken = Jwt.generateAccessToken(userId=str(existedUser['_id']), role=existedUser['role'])
            refreshToken = Jwt.generateRefreshToken(userId=str(existedUser['_id']), role=existedUser['role'])
            return GeneralWrapper.successResult(UsersWrapper.loginResult(existedUser, accessToken, refreshToken))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def refreshToken(refreshToken):
        try:
            GeneralHelper.checkString(refreshToken, ResponseCodes.invalidToken)
            accessToken = Jwt.checkRefreshTokenAndGenerateNewAccessToken(token=refreshToken)
            result = {
                "accessToken" : accessToken,
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def resendVerificationCode(email):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email, True, False)
            if not (existedUser['verifiedAt'] is None):
                raise BusinessException(ResponseCodes.alreadyVerifiedUser)      
            Email.sendVerificationEmail(existedUser['email'], existedUser['verificationCode'])
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def verify(email, code, password):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            #GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(code, ResponseCodes.emptyVerificationCode)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email, True, True)
            if not (existedUser['verifiedAt'] is None):
                raise BusinessException(ResponseCodes.alreadyVerifiedUser)  
            if existedUser['verificationCode'] != code:
                raise BusinessException(ResponseCodes.verificationCodeNotMatch)
            if not GeneralHelper.isValidString(password):
                password = existedUser['password']
            else:
                password = PasswordHelper.hash(password)
            UsersDataAccess.verify(db, existedUser['_id'], password)
            accessToken = Jwt.generateAccessToken(userId=str(existedUser['_id']), role=existedUser['role'])
            refreshToken = Jwt.generateRefreshToken(userId=str(existedUser['_id']), role=existedUser['role'])
            return GeneralWrapper.successResult(UsersWrapper.loginResult(existedUser, accessToken, refreshToken))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    '''
    @staticmethod
    def forgetPasswordFirstStep(email):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            query = {
                "email" : email,
                "deleted_at" : None
            }
            existedUser = db.users.find_one(query)
            if existedUser is None:
                raise BusinessException(ResponseCodes.userNotFound)
            forgetPasswordCode = str(randint(100000, 999999))
            forgetPasswordRequest = {
                "user_id" : existedUser['_id'],
                "email" : existedUser['email'],
                "code" : forgetPasswordCode,
                "created_at" : datetime.now(tz=timezone.utc),
                "deleted_at" : None
            }
            insertResult = db.forget_password_requests.insert_one(forgetPasswordRequest)
            Email.sendForgetPasswordEmail(email, forgetPasswordCode)
            result = {
                "request_forget_password_id" : str(insertResult.inserted_id)
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def resendForgetPasswordCode(requestId):
        try:
            GeneralHelper.checkString(requestId, ResponseCodes.emptyOrInvalidForgetPasswordRequestId)
            id = GeneralHelper.getObjectId(requestId)
            dbConnection = (Database())
            db = dbConnection.db
            query = {
                "_id" : id,
                "deleted_at" : None
            }
            existedRequest = db.forget_password_requests.find_one(query)
            if existedRequest is None:
                raise BusinessException(ResponseCodes.forgetPasswordRequestNotFound)
            BusinessAuth.__sendVerificationEmail(existedRequest["email"], existedRequest["code"])
            result = {
                "request_forget_password_id" : requestId
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def forgetPasswordSecondStep(requestId, code, password):
        try:
            GeneralHelper.checkString(requestId, ResponseCodes.emptyOrInvalidForgetPasswordRequestId)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(code, ResponseCodes.emptyOrInvalidForgetPasswordCode)
            id = GeneralHelper.getObjectId(requestId)
            dbConnection = (Database())
            db = dbConnection.db
            query = {
                "_id" : id,
                "deleted_at" : None
            }
            existedRequest = db.forget_password_requests.find_one(query)
            if existedRequest is None:
                raise BusinessException(ResponseCodes.forgetPasswordRequestNotFound)
            if existedRequest['code'] != code:
                raise BusinessException(ResponseCodes.forgetPasswordCodeNotMatch)
            db.forget_password_requests.update_one(query, {"$set": {"deleted_at" : datetime.now(tz=timezone.utc)}})
            db.users.update_one({"_id" : existedRequest['user_id']}, {"$set": {"password" : GeneralHelper.hash(password)}})
            return BusinessAuth.login(existedRequest['email'], password)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])


    '''