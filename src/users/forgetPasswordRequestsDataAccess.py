from datetime import timezone,datetime
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from src.shared.generalHelper import GeneralHelper

class ForgetPasswordRequestsDataAccess:
    @staticmethod
    def add(db, userId, userEmail, code):
        forgetPasswordRequest = {
            "userId" : userId,
            "email" : userEmail,
            "code" : code,
            "createdAt" : datetime.now(tz=timezone.utc),
            "deletedAt" : None
        }
        return db.forget_password_requests.insert_one(forgetPasswordRequest)

    @staticmethod
    def getById(db, id):
        query = {
            "_id" : id,
            "deletedAt" : None
        }
        existedRequest = db.forget_password_requests.find_one(query)
        if existedRequest is None:
            raise BusinessException(ResponseCodes.forgetPasswordRequestNotFound)
        return existedRequest

    @staticmethod
    def delete(db, id):
        db.forget_password_requests.update_one({'_id' : id}, {"$set": {"deletedAt" : datetime.now(tz=timezone.utc)}})
