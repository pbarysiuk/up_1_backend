from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from datetime import timezone,datetime
from src.shared.generalHelper import GeneralHelper

class XdlDataAccess:
    status = {
        "deleted" : 0,
        "approved" : 1,
        "rejected" : 2,
        "pending" : 3
    }


    @staticmethod
    def add(db, filePath, drugs):
        nowDate = datetime.now(tz=timezone.utc)
        i = 0
        while i < len(drugs):
            xml = drugs[i]['xml']
            text = drugs[i]['text']
            name = drugs[i]['name']
            xdl = {
                "name" : name,
                "nameLower" : name.lower(),
                "filePath" : filePath,
                "createdAt" : nowDate,
                "createdBy" : None,
                "status" : XdlDataAccess.status["pending"],
                "statusChangedAt" : None,
                "statusChangedBy" : None,
                "xml" : xml,
                "text" : text
            }
            db.xdl.insert_one(xdl)
            i += 1
        return

    @staticmethod
    def getList(db, criteria, pageNumber, pageSize):
        projection = {
            "name" : 1,
            "title" : 1,
            "filePath" : 1,
            "createdAt" : 1,
            "createdBy" : 1,
            "status" :1,
            "statusChangedAt" : 1,
            "statusChangedBy" : 1
        }
        query = {
            "name" : {
                "$regex": criteria,
                "$options": "i"
            },
            'status': { "$ne" : XdlDataAccess.status['deleted'] }
        }
        items = db.xdl.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl.count_documents(query)
        return count, items

    @staticmethod
    def getDetails(db, id, throwExceptionIfNotFound = True):
        existedXdl = XdlDataAccess.getById(db, id, throwExceptionIfNotFound, True)
        if existedXdl is None:
            return None
        return existedXdl

    @staticmethod
    def getById(db, id, throwExceptionIfNotFound = True, details = False):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'status': { "$ne" : XdlDataAccess.status['deleted'] }
        }
        projection = {
            "name" : 1
        }
        existedXdl = None
        if details:
            existedXdl = db.xdl.find_one(query)
        else:
            existedXdl = db.xdl.find_one(query, projection)
        if existedXdl is None and throwExceptionIfNotFound:
            raise BusinessException(ResponseCodes.xdlNotFound)
        return existedXdl

    @staticmethod
    def changeStatus(db, existedXdl, approve, drugName, title, userId):
        query = {
            "_id" : existedXdl['_id']
        }
        newStatus = None
        if approve:
            newStatus = XdlDataAccess.status['approved']
        else:
            newStatus = XdlDataAccess.status['rejected']
        updatedFields = {
            "$set" : {
                "name" : drugName,
                'title' : title,
                "nameLower" : drugName.lower(),
                "status" : newStatus,
                "statusChangedAt" : datetime.now(tz=timezone.utc),
                "statusChangedBy" : userId
            }
        }
        db.xdl.update_one(query, updatedFields)

    @staticmethod
    def search(db, criteria, pageNumber, pageSize):
        query = {
            "nameLower" : {
                "$regex": criteria.lower(),
            } ,
            "status" : XdlDataAccess.status['approved']
        }
        projection = {
            "name" : 1,
            "title" : 1,
            "filePath" : 1,
            "createdAt" : 1,
            "createdBy" : 1,
            "statusChangedAt" : 1,
            "statusChangedBy" : 1,
            "text" : 1,
            "xml" : 1
        }
        items = db.xdl.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl.count_documents(query)
        return count, items



