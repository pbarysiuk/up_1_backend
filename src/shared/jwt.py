import jwt
from datetime import timezone,datetime,timedelta
from os import environ
from src.shared.generalHelper import GeneralHelper
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.lambdaHelper import LambdaHelper

class Jwt:
    __algorithm="RS256"
    __accessTokenDuration=30 #access token is valid for 30 min
    __refreshTokenDuration=43200 #refresh token is valid for a month

    userRole = "user"
    adminRole = "admin"
    roles = [userRole, adminRole]
    
    @staticmethod
    def __generateToken(payload, secret):
        return jwt.encode(payload, secret.encode('utf-8'), algorithm=Jwt.__algorithm)

    @staticmethod
    def __checkToken(token, secret):
        try:
            return jwt.decode(token, secret.encode('utf-8'), algorithms=Jwt.__algorithm)
        except Exception as e:
            raise BusinessException(ResponseCodes.invalidToken)

    @staticmethod
    def __generatePayload(userId, role, duration):
        payload = {
            "id" : userId,
            "role" : role,
            GeneralHelper.generateGUID() : GeneralHelper.generateGUID(),
            "expire": int((datetime.now(tz=timezone.utc) + timedelta(minutes=duration)).timestamp())        
        }
        return payload

    @staticmethod
    def generateAccessToken(userId, role):
        payload = Jwt.__generatePayload(userId=userId, role=role, duration=Jwt.__accessTokenDuration)
        secret = LambdaHelper.getValueFromParameterStore(envKey='PS_ACCESS_TOKEN_PRIVATE', defaultEnvKey='ACCESS_TOKEN_PRIVATE')
        return Jwt.__generateToken(payload=payload, secret=secret)

    @staticmethod
    def checkAccessToken(token, allowedRoles = []):
        secret = LambdaHelper.getValueFromParameterStore(envKey='PS_ACCESS_TOKEN_PUBLIC', defaultEnvKey='ACCESS_TOKEN_PUBLIC')
        payload = Jwt.__checkToken(token, secret=secret)
        if payload["expire"] < int(datetime.now(tz=timezone.utc).timestamp()) :
            raise BusinessException(ResponseCodes.expiredToken)
        if len(allowedRoles) > 0 and not (payload["role"] in allowedRoles) :
             raise BusinessException(ResponseCodes.lackOfPrivileges)
        return payload

    @staticmethod
    def generateRefreshToken(userId, role):
        payload = Jwt.__generatePayload(userId=userId, role=role, duration=Jwt.__refreshTokenDuration)
        secret = LambdaHelper.getValueFromParameterStore(envKey='PS_REFRESH_TOKEN_PRIVATE', defaultEnvKey='REFRESH_TOKEN_PRIVATE')
        return Jwt.__generateToken(payload=payload, secret=secret)

    @staticmethod
    def checkRefreshTokenAndGenerateNewAccessToken(token):
        secret = LambdaHelper.getValueFromParameterStore(envKey='PS_REFRESH_TOKEN_PUBLIC', defaultEnvKey='REFRESH_TOKEN_PUBLIC')
        payload = Jwt.__checkToken(token, secret=secret)
        if payload["expire"] < int(datetime.now(tz=timezone.utc).timestamp()):
            raise BusinessException(ResponseCodes.expiredToken)
        return Jwt.generateAccessToken(payload["id"], payload["role"])



