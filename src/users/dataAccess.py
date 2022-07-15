from datetime import timezone,datetime
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper

class UsersDataAccess:
    @staticmethod
    def insertUser(db, name, email, password, role, image, verificationCode, isVerified = False):
        lastChangePassword = None
        if isVerified:
            lastChangePassword = datetime.now(tz=timezone.utc)
        user = {
            "name" : name,
            "email" : email,
            "password" : password,
            "role" : role,
            "image" : image,
            "verificationCode" : verificationCode,
            "verifiedAt" :  datetime.now(tz=timezone.utc),
            "createdAt" : datetime.now(tz=timezone.utc),
            "updatedAt" : None,
            "deletedAt" : None,
            "lastChangePassword" : lastChangePassword
        }
        return db.users.insert_one(user)

    @staticmethod
    def checkUniqueEmail(db, email, id = None):
        query = {
            "email" : email,
            'deletedAt': None,
            "_id" : {
                '$ne' : GeneralHelper.getObjectId(id=id)
            }
        }
        count = db.users.count_documents(query)
        if count > 0:
            raise BusinessException(ResponseCodes.duplicateEmail)

    @staticmethod
    def getById(db, id, throwExceptionIfNotFound = True, includePassword = False):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'deletedAt': None
        }
        projection = {
            "name" : 1,
            "email" : 1,
            "role" : 1,
            "image" : 1,
            "verifiedAt" : 1,
            "verificationCode" : 1,
            "createdAt" : 1,
            "lastChangePassword" : 1
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
    def getByEmail(db, email, throwExceptionIfNotFound = True, includePassword = False):
        query = {
            "email" : email,
            'deletedAt': None
        }
        projection = {
            "name" : 1,
            "email" : 1,
            "role" : 1,
            "image" : 1,
            "verifiedAt" : 1,
            "verificationCode" : 1,
            "createdAt" : 1,
            "lastChangePassword" : 1
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
    def verify(db, id, password):
        query = {
            '_id' : id
        }
        setQuery = {
            'password' : password,
            'verifiedAt' : datetime.now(tz=timezone.utc)
        }
        db.users.update_one(query, {"$set": setQuery})
        return

    @staticmethod
    def update(db, id, name, email, role, image):
        setQuery={
                "name" : name,
                "email" : email,
                "role" : role,
                "image" : image,
                "updatedAt" : datetime.now(tz=timezone.utc)
            }
        db.users.update_one({"_id" : id}, {"$set": setQuery})

    @staticmethod
    def delete(db, id):
        setQuery={
                "deletedAt" : datetime.now(tz=timezone.utc)
            }
        db.users.update_one({"_id" : id}, {"$set": setQuery})

    @staticmethod
    def getCountOfNotDeletedUsers(db):
        query = {
            'deletedAt': None,
            'role' : 'admin'
        }
        count = db.users.count_documents(query)
        return count

    @staticmethod
    def getList(db, criteria, pageNumber, pageSize):
        projection = {
            "name" : 1,
            "email" : 1,
            "role" : 1,
            "image" : 1,
            "createdAt" : 1
        }
        query = {
            "$and" : [
                {
                    "deletedAt" : None
                }
            ]
        }
        if (GeneralHelper.isValidString(criteria)):
            query["$and"].append({
                "$or" : [
                    {
                        "name" : {
                            "$regex": criteria,
                            "$options": "i"
                        }
                    },
                    {
                        "email" : {
                            "$regex": criteria,
                            "$options": "i"
                        }
                    }
                ]
            })
        items = db.users.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.users.count_documents(query)
        return count, items

    @staticmethod
    def addForgetPasswordRequest(db, userId, userEmail, code):
        forgetPasswordRequest = {
            "userId" : userId,
            "email" : userEmail,
            "code" : code,
            "createdAt" : datetime.now(tz=timezone.utc),
            "deletedAt" : None
        }
        return db.forget_password_requests.insert_one(forgetPasswordRequest)

    @staticmethod
    def getForgetPaswordRequest(db, id):
        query = {
            "_id" : id,
            "deletedAt" : None
        }
        existedRequest = db.forget_password_requests.find_one(query)
        if existedRequest is None:
            raise BusinessException(ResponseCodes.forgetPasswordRequestNotFound)
        return existedRequest

    @staticmethod
    def deleteForgetPasswordRequest(db, id):
        db.forget_password_requests.update_one({'_id' : id}, {"$set": {"deletedAt" : datetime.now(tz=timezone.utc)}})

    @staticmethod
    def updatePassword(db, id, password):
        query = {
            '_id' : id,
            'deletedAt' : None
        }
        updatedFields = {
            'password' : password,
            'lastChangePassword' : datetime.now(tz=timezone.utc)
        }
        db.users.update_one(query, {"$set": updatedFields})


    