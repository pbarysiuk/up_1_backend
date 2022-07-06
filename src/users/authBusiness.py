from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.jwt import Jwt
import traceback
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
            if existedUser['lastChangePassword'] is None:
                firstTimeResetPasswordToken = Jwt.generateFirstTimeResetPasswordToken(userId=str(existedUser['_id']))
                result = {
                    "firstTimeResetPasswordToken" : firstTimeResetPasswordToken
                }
                return GeneralWrapper.successResult(result)   
            accessToken = Jwt.generateAccessToken(userId=str(existedUser['_id']), role=existedUser['role'])
            refreshToken = Jwt.generateRefreshToken(userId=str(existedUser['_id']), role=existedUser['role'])
            return GeneralWrapper.successResult(UsersWrapper.loginResult(existedUser, accessToken, refreshToken))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def resetPasswordFirstTime(resetPasswordToken, password):
        try:
            GeneralHelper.checkString(resetPasswordToken, ResponseCodes.invalidToken)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            payload = Jwt.checkFirstTimeResetPasswordToken(token=resetPasswordToken)
            userId = GeneralHelper.getObjectId(payload["id"])
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getById(db, userId)
            if not (existedUser['lastChangePassword'] is None):
                raise BusinessException(ResponseCodes.alreadyResettedPasswordFirstTime)
            UsersDataAccess.updatePassword(db, existedUser['_id'], PasswordHelper.hash(password))    
            return GeneralWrapper.successResult(None)
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
            return GeneralWrapper.generalErrorResult(e)

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
            return GeneralWrapper.generalErrorResult(e)
    
    @staticmethod
    def forgetPasswordFirstStep(email):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email)
            forgetPasswordCode = GeneralHelper.generateCode()
            insertResult = UsersDataAccess.addForgetPasswordRequest(db, existedUser['_id'], existedUser['email'], forgetPasswordCode)
            Email.sendForgetPasswordEmail(email, forgetPasswordCode)
            return GeneralWrapper.successResult(UsersWrapper.forgetPasswordResult(insertResult.inserted_id))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def resendForgetPasswordCode(requestId):
        try:
            GeneralHelper.checkString(requestId, ResponseCodes.emptyOrInvalidForgetPasswordRequestId)
            id = GeneralHelper.getObjectId(requestId)
            dbConnection = (Database())
            db = dbConnection.db
            existedRequest = UsersDataAccess.getForgetPaswordRequest(db, id)
            Email.sendForgetPasswordEmail(existedRequest['email'], existedRequest['code'])
            return GeneralWrapper.successResult(UsersWrapper.forgetPasswordResult(existedRequest['_id']))
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def forgetPasswordSecondStep(requestId, code, password):
        try:
            GeneralHelper.checkString(requestId, ResponseCodes.emptyOrInvalidForgetPasswordRequestId)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkString(code, ResponseCodes.emptyOrInvalidForgetPasswordCode)
            id = GeneralHelper.getObjectId(requestId)
            dbConnection = (Database())
            db = dbConnection.db
            existedRequest = UsersDataAccess.getForgetPaswordRequest(db, id)
            if existedRequest['code'] != code:
                raise BusinessException(ResponseCodes.forgetPasswordCodeNotMatch)
            existedUser = UsersDataAccess.getById(db, existedRequest['userId'])
            if existedUser['verifiedAt'] is None:
                UsersDataAccess.updatePassword(db, existedRequest['userId'],  PasswordHelper.hash(password), True)
            else:
                UsersDataAccess.updatePassword(db, existedRequest['userId'],  PasswordHelper.hash(password))
            UsersDataAccess.deleteForgetPasswordRequest(db, existedRequest['_id'])
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

