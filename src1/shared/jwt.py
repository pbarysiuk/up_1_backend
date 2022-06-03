import jwt
from datetime import timezone,datetime,timedelta
from os import environ
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes

class Jwt:
    __algorithm="HS256"
    __accessTokenDuration=30 #access token is valid for 30 min
    __refreshTokenDuration=43200 #refresh token is valid for a month

    userRole = "user"
    adminRole = "admin"
    roles = [userRole, adminRole]
    
    @staticmethod
    def __generateToken(payload, secret):
        return jwt.encode(payload, secret, algorithm=Jwt.__algorithm)

    @staticmethod
    def __checkToken(token, secret):
        try:
            return jwt.decode(token, secret, algorithms=Jwt.__algorithm)
        except Exception as e:
            raise BusinessException(ResponseCodes.invalidToken)

    @staticmethod
    def __generatePayload(userId, role, duration):
        payload = {
            "id" : userId,
            "role" : role,
            "expire": int((datetime.now(tz=timezone.utc) + timedelta(minutes=duration)).timestamp())        
        }
        return payload

    @staticmethod
    def generateAccessToken(userId, role):
        payload = Jwt.__generatePayload(userId=userId, role=role, duration=Jwt.__accessTokenDuration)
        return Jwt.__generateToken(payload=payload, secret=environ.get('ACCESS_TOKEN_SECRET'))

    @staticmethod
    def checkAccessToken(token, allowedRoles = []):
        payload = Jwt.__checkToken(token, secret=environ.get('ACCESS_TOKEN_SECRET'))
        if payload["expire"] < int(datetime.now(tz=timezone.utc).timestamp()) :
            raise BusinessException(ResponseCodes.expiredToken)
        if len(allowedRoles) > 0 and not (payload["role"] in allowedRoles) :
             raise BusinessException(ResponseCodes.lackOfPrivileges)
        return payload

    @staticmethod
    def generateRefreshToken(userId, role):
        payload = Jwt.__generatePayload(userId=userId, role=role, duration=Jwt.__refreshTokenDuration)
        return Jwt.__generateToken(payload=payload, secret=environ.get('REFRESH_TOKEN_SECRET'))

    @staticmethod
    def checkRefreshTokenAndGenerateNewAccessToken(token):
        payload = Jwt.__checkToken(token, secret=environ.get('REFRESH_TOKEN_SECRET'))
        if payload["expire"] < int(datetime.now(tz=timezone.utc).timestamp()):
            raise BusinessException(ResponseCodes.expiredToken)
        return Jwt.generateAccessToken(payload["id"], payload["role"])