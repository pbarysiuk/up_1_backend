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
            xdlDetails = {
                "xml" : xml,
                "text" : text
            }
            insertResult = db.xdl_details.insert_one(xdlDetails)
            xdl = {
                "detailsId" : insertResult.inserted_id,
                "name" : name,
                "filePath" : filePath,
                "createdAt" : nowDate,
                "createdBy" : None,
                "status" : XdlDataAccess.status["pending"],
                "statusChangedAt" : None,
                "statusChangedBy" : None
            }
            db.xdl.insert_one(xdl)
            i += 1
        return

    @staticmethod
    def getList(db, criteria, pageNumber, pageSize):
        projection = {
            "name" : 1,
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
        existedXdl = XdlDataAccess.getById(db, id, throwExceptionIfNotFound)
        if existedXdl is None:
            return None
        projection = {
            "xml" : 1,
            "text" : 1
        }
        result = db.xdl_details.find_one({'_id' : existedXdl['detailsId']}, projection)
        result ['_id'] =  existedXdl['_id']
        result ['createdBy'] =  existedXdl['createdBy']
        result ['status'] = existedXdl['status']
        result ['statusChangedAt'] = existedXdl['statusChangedAt']
        result ['statusChangedBy'] = existedXdl['statusChangedBy']
        result ['createdAt'] =  existedXdl['createdAt']
        result ['filePath'] =  existedXdl['filePath']
        result ['name'] =  existedXdl['name']
        return result

    @staticmethod
    def getById(db, id, throwExceptionIfNotFound = True):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'status': { "$ne" : XdlDataAccess.status['deleted'] }
        }
        existedXdl = db.xdl.find_one(query)
        if existedXdl is None and throwExceptionIfNotFound:
            raise BusinessException(ResponseCodes.xdlNotFound)
        return existedXdl

    @staticmethod
    def changeStatus(db, existedXdl, approve, drugName, userId):
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
                "status" : newStatus,
                "statusChangedAt" : datetime.now(tz=timezone.utc),
                "statusChangedBy" : userId
            }
        }
        db.xdl.update_one(query, updatedFields)

    @staticmethod
    def search(db, criteria, pageNumber, pageSize):
        query = {
            "name" : {
                "$regex": criteria,
                "$options": "i"
            },
            "status" : XdlDataAccess.status['approved']
        }
        projection = {
            "name" : 1,
            "filePath" : 1,
            "createdAt" : 1,
            "createdBy" : 1,
            "statusChangedAt" : 1,
            "statusChangedBy" : 1
        }
        items = db.xdl.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl.count_documents(query)
        return count, items



