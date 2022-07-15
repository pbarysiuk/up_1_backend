from datetime import timezone,datetime
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper

class UsersDataAccess:
    status = {
        'approved' : 1,
        'pending' : 2,
        'deleted' : 0
    }

    @staticmethod
    def addDefault(db, name, email, password, role, image, keyId, keyValue):
        nowDate = datetime.now(tz=timezone.utc)
        apiKeyObject = {
            'id' : keyId,
            'value' : keyValue
        }
        user = {
            "name" : name,
            "email" : email,
            "password" : password,
            "role" : role,
            "image" : image,
            "verificationCode" : '',
            "linkedInId" : None,
            "apiKey" : apiKeyObject,
            "createdBy" : None,
            "verifiedAt" :  nowDate,
            "lastChangePasswordAt" : nowDate,
            "status" :  UsersDataAccess.status['approved'],
            "createdAt" : nowDate,
            "updatedAt" : None,
            "deletedAt" : None,
            "approvedAt" : nowDate
        }
        return db.users.insert_one(user)

    @staticmethod
    def __addNew(db, name, email, password, role, image, verificationCode, linkedInId, adminId):
        nowDate = datetime.now(tz=timezone.utc)
        lastChangePasswordAt = nowDate
        verifiedAt = None
        approvedAt = None
        status = UsersDataAccess.status['pending']
        if not (adminId is None):
            lastChangePasswordAt = None
            verifiedAt = nowDate
            approvedAt = nowDate
            status = UsersDataAccess.status['approved']
        elif not (linkedInId is None):
            verifiedAt = nowDate
        user = {
            "name" : name,
            "email" : email,
            "password" : password,
            "role" : role,
            "image" : image,
            "verificationCode" : verificationCode,
            "linkedInId" : linkedInId,
            "apiKey" : {},
            "createdBy" : adminId,
            "verifiedAt" :  verifiedAt,
            "lastChangePasswordAt" : lastChangePasswordAt,
            "status" : status,
            "createdAt" : datetime.now(tz=timezone.utc),
            "updatedAt" : None,
            "deletedAt" : None,
            "approvedAt" : approvedAt
        }
        return db.users.insert_one(user)

    @staticmethod
    def __forceDelete(db, id):
        db.users.delete_one({'_id' : id})

    @staticmethod
    def __getNotVerifiedByEmail(db, email):
        existedUser = db.users.find_one({
            "email" : email,
            "verifiedAt" : None
        }, {'_id' : 1})
        return existedUser
    
    @staticmethod
    def add(db, name, email, password, role, image, verificationCode, linkedInId, adminId):
        existedUser = UsersDataAccess.__getNotVerifiedByEmail(db, email)
        if not (existedUser is None):
            UsersDataAccess.__forceDelete(db, existedUser['_id'])
        return UsersDataAccess.__addNew(db, name, email, password, role, image, verificationCode, linkedInId, adminId)
    
    @staticmethod
    def checkUniqueEmail(db, email, id = None):
        query = {
            "email" : email,
            "status": { '$ne' : UsersDataAccess.status['deleted'] },
            "verifiedAt" : { '$ne' : None  },
            "_id" : { '$ne' : GeneralHelper.getObjectId(id=id)  }
        }
        count = db.users.count_documents(query)
        if count > 0:
            raise BusinessException(ResponseCodes.duplicateEmail)

    @staticmethod
    def updateApiKey(db, id, keyId, keyValue):
        apiKeyObject = {
            'id' : keyId,
            'value' : keyValue
        }
        setQuery = {
            'apiKey' : apiKeyObject
        }
        db.users.update_one({"_id" : id}, {"$set": setQuery})

    @staticmethod
    def getByEmail(db, email, throwExceptionIfNotFound = True, includePassword = False):
        query = {
            "email" : email,
            "status": { '$ne' : UsersDataAccess.status['deleted'] }
        }
        projection = {
            "name" : 1,
            "email" : 1,
            "role" : 1,
            "image" : 1,
            "linkedInId" : 1,
            "apiKey" : 1,
            "verifiedAt" : 1,
            "verificationCode" : 1,
            "createdAt" : 1,
            "lastChangePasswordAt" : 1,
            "status" : 1
        }
        if includePassword:
            projection["password"] = 1
        existedUser = db.users.find_one(query, projection)
        if existedUser is None:
            if throwExceptionIfNotFound:
                raise BusinessException(ResponseCodes.userNotFound)
            return None
        return existedUser
