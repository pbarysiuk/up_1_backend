
'''


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

'''