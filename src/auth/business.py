from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.exceptions.responseMessages import ResponseMessages
from src.shared.generalHelper import GeneralHelper
from src.shared.generalWrapper import GeneralWrapper
from src.shared import database
from src.shared.jwt import Jwt
import traceback
from os import environ
import boto3
from botocore.exceptions import ClientError
from random import randint
from datetime import timezone,datetime

class BusinessAuth:
    @staticmethod
    def __sendVerificationEmail(toEmail, verificationCode):
        sender = environ.get('EMAIL_SENDER')
        awsRegion=environ.get('EMAIL_AWS_REGION')
        charset = "utf-8"
        awsCred = {
            "aws_access_key_id":environ.get('AWS_ACCESS_KEY'),
            "aws_secret_access_key":environ.get('AWS_SECRET_KEY') 
        }
        client = boto3.client('ses',**awsCred, region_name=awsRegion)
        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": [
                        toEmail,
                    ],
                },
                Message={
                    "Body": {
                        "Text": {
                            "Charset": charset,
                            "Data": "Your reset password is: " + str(verificationCode),
                        }
                    },
                    "Subject": {
                        "Charset": charset,
                        "Data": "Prepaire forget password",
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        return
        
    @staticmethod
    def login(email, password):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkString(password, ResponseCodes.emptyOrInvalidPassword)
            GeneralHelper.checkEmailFormat(email)
            db = database.get_connection()
            query = {
                "email" : email,
                "password" : GeneralHelper.hash(password),
                "deleted_at" : None
            }
            projection = {
                "name" : 1,
                "email" : 1,
                "role" : 1,
                "created_at" : 1,
                "updated_at" : 1
            }
            existedUser = db.users.find_one(query, projection)
            if existedUser is None:
                raise BusinessException(ResponseCodes.wrongEmailOrPassword)           
            accessToken = Jwt.generateAccessToken(userId=str(existedUser['_id']), role=existedUser['role'])
            refreshToken = Jwt.generateRefreshToken(userId=str(existedUser['_id']), role=existedUser['role'])
            result = {
                "access_token" : accessToken,
                "refresh_token" : refreshToken,
                "user" : existedUser
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def refreshToken(refreshToken):
        try:
            GeneralHelper.checkString(refreshToken, ResponseCodes.invalidToken)
            accessToken = Jwt.checkRefreshTokenAndGenerateNewAccessToken(token=refreshToken)
            result = {
                "access_token" : accessToken,
            }
            return GeneralWrapper.successResult(result)
        except BusinessException as e:
            return GeneralWrapper.errorResult(e.code, e.message)
        except Exception as e:
            traceback.print_exc()
            return GeneralWrapper.errorResult(ResponseCodes.generalError, ResponseMessages.english[ResponseCodes.generalError])

    @staticmethod
    def forgetPasswordFirstStep(email):
        try:
            GeneralHelper.checkString(email, ResponseCodes.emptyOrInvalidEmail)
            GeneralHelper.checkEmailFormat(email)
            db = database.get_connection()
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
            BusinessAuth.__sendVerificationEmail(email, forgetPasswordCode)
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
            db = database.get_connection()
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
            db = database.get_connection()
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