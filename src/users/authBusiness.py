from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared.jwt import Jwt
import traceback
from src.shared.emails import Email
from src.shared.database import Database
from src.users.usersDataAccess import UsersDataAccess
from src.users.forgetPasswordRequestsDataAccess import ForgetPasswordRequestsDataAccess
from src.shared.passwordHelper import PasswordHelper
from src.users.wrapper import UsersWrapper

class AuthBusiness:
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
            if existedUser['verifiedAt'] is None:
                raise BusinessException(ResponseCodes.notVerifiedUser)
            if existedUser['status'] != UsersDataAccess.status['approved']:
                raise BusinessException(ResponseCodes.notApprovedUser)
            PasswordHelper.checkPassword(existedUser['password'], password, ResponseCodes.wrongEmailOrPassword)
            if existedUser['lastChangePassword'] is None:
                firstTimeResetPasswordToken = Jwt.generateFirstTimeResetPasswordToken(userId=str(existedUser['_id']))
                return GeneralWrapper.successResult(UsersWrapper.resetPasswordFirstTimeTokenResult(firstTimeResetPasswordToken))   
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
            AuthBusiness.__checkEligibilityForVerify(existedUser)    
            Email.sendVerificationEmail(existedUser['email'], existedUser['verificationCode'])
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def verify(email, code):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(code, ResponseCodes.emptyVerificationCode)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email, True, True)
            AuthBusiness.__checkEligibilityForVerify(existedUser)
            if existedUser['verificationCode'] != code:
                raise BusinessException(ResponseCodes.verificationCodeNotMatch)
            UsersDataAccess.verify(db, existedUser['_id'])
            return GeneralWrapper.successResult(None)
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
            AuthBusiness.__checkEligibilityForForgetPassword(existedUser)
            forgetPasswordCode = GeneralHelper.generateCode()
            insertResult = ForgetPasswordRequestsDataAccess.add(db, existedUser['_id'], existedUser['email'], forgetPasswordCode)
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
            existedRequest = ForgetPasswordRequestsDataAccess.getById(db, id)
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
            existedRequest = ForgetPasswordRequestsDataAccess.getById(db, id)
            if existedRequest['code'] != code:
                raise BusinessException(ResponseCodes.forgetPasswordCodeNotMatch)
            existedUser = UsersDataAccess.getById(db, existedRequest['userId'])
            AuthBusiness.__checkEligibilityForForgetPassword(existedUser)
            UsersDataAccess.updatePassword(db, existedRequest['userId'],  PasswordHelper.hash(password))
            ForgetPasswordRequestsDataAccess.delete(db, existedRequest['_id'])
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def register(name, email, password, image):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(name, ResponseCodes.emptyOrInvalidName)
            GeneralHelper.checkEmailFormat(email)
            dbConnection = (Database())
            db = dbConnection.db
            UsersDataAccess.checkUniqueEmail(db, email)
            verificatioCode = GeneralHelper.generateCode()
            insertResult = UsersDataAccess.add(db, name, email, PasswordHelper.hash(password), Jwt.userRole, image, verificatioCode, None, None)
            Email.sendVerificationEmail(email, verificatioCode)
            return GeneralWrapper.successResult(None)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)

    @staticmethod
    def loginWithThirdParty(thrirdPartyType, thirdPartyToken):
        try:
            GeneralHelper.checkString(thrirdPartyType, ResponseCodes.emptyOrInvalidThirdPartyType)
            GeneralHelper.checkString(thirdPartyToken, ResponseCodes.emptyOrInvalidThirdPartyToken)
            allThirdPartyTypes = ['linkedin', 'apple']
            thirdPartyToken = thirdPartyToken.lower()
            if not (thirdPartyToken in allThirdPartyTypes):
                raise BusinessException(ResponseCodes.emptyOrInvalidThirdPartyType)
            #here we should decode the token and get email, name, image, third party id
            email = 'habibfrancis95@gmail.com'
            name = 'habib francis'
            image = None 
            thrirdPartyId = '12345'
            dbConnection = (Database())
            db = dbConnection.db
            existedUser = UsersDataAccess.getByEmail(db, email, False, False)
            if existedUser is None or existedUser['verifiedAt'] is None:
                UsersDataAccess.add(db, name, email, None, Jwt.userRole, image, None, {thrirdPartyType : thrirdPartyId}, None)
                return GeneralWrapper.successResult(None)
            userChanged = False
            if (not (existedUser['thirdPartyLogin'].get(thrirdPartyType) is None)) or existedUser['thirdPartyLogin'].get(thrirdPartyType) != thrirdPartyId:
                #update thrid party login for user
                userChanged = True
                thirdPartyLogin = existedUser['thirdPartyLogin']
                thirdPartyLogin[thrirdPartyType] = thrirdPartyId
                UsersDataAccess.updateThirdPartyLogin(db, existedUser['_id'], thirdPartyLogin)
            if existedUser['status'] != UsersDataAccess.status['approved']:
                raise BusinessException(ResponseCodes.notApprovedUser)
            if userChanged:
                existedUser = UsersDataAccess.getById(db, existedUser['_id'])
            accessToken = Jwt.generateAccessToken(userId=str(existedUser['_id']), role=existedUser['role'])
            refreshToken = Jwt.generateRefreshToken(userId=str(existedUser['_id']), role=existedUser['role'])
            return GeneralWrapper.successResult(UsersWrapper.loginResult(existedUser, accessToken, refreshToken))          
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.generalErrorResult(e)



    @staticmethod
    def __checkEligibilityForForgetPassword(existedUser):
        if existedUser['verifiedAt'] is None:
            raise BusinessException(ResponseCodes.notVerifiedUser)
        if existedUser['status'] != UsersDataAccess.status['approved']:
            raise BusinessException(ResponseCodes.notApprovedUser)

    @staticmethod
    def __checkEligibilityForVerify(existedUser):
        if not (existedUser['verifiedAt'] is None):
            raise BusinessException(ResponseCodes.alreadyVerifiedUser) 
        if existedUser['status'] == UsersDataAccess.status['deactivated']:
            raise BusinessException(ResponseCodes.deactivatedUser)     
