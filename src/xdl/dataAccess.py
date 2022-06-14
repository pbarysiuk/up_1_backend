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
                "allDrugsNames" : [name],
                "approvedDrugsNames" : [],
                "filePath" : filePath,
                "xml" : xml,
                "text" : text,
                "createdAt" : nowDate
            }
            insertResult = db.xdl.insert_one(xdl)
            xdlList = {
                "xdlId" : insertResult.inserted_id,
                "name" : name,
                "filePath" : filePath,
                "createdAt" : nowDate,
                "createdBy" : None,
                "status" : XdlDataAccess.status["pending"],
                "statusChangedAt" : None,
                "statusChangedBy" : None
            }
            db.xdl_list.insert_one(xdlList)
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
        items = db.xdl_list.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl_list.count_documents(query)
        return count, items

    @staticmethod
    def getDetails(db, id, throwExceptionIfNotFound = True):
        existedXdlList = XdlDataAccess.getById(db, id, throwExceptionIfNotFound)
        if existedXdlList is None:
            return None
        projection = {
            "allDrugsNames" : 1,
            "approvedDrugsNames" : 1,
            "filePath" : 1,
            "xml" : 1,
            "text" : 1,
            "createdAt" : 1,
            '_id' : 0
        }
        result = db.xdl.find_one({'_id' : existedXdlList['xdlId']}, projection)
        result ['_id'] =  existedXdlList['_id']
        result ['createdBy'] =  existedXdlList['createdBy']
        result ['status'] = existedXdlList['status']
        result ['statusChangedAt'] = existedXdlList['statusChangedAt']
        result ['statusChangedBy'] = existedXdlList['statusChangedBy']
        return result

    @staticmethod
    def getById(db, id, throwExceptionIfNotFound = True):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'status': { "$ne" : XdlDataAccess.status['deleted'] }
        }
        existedXdl = db.xdl_list.find_one(query)
        if existedXdl is None and throwExceptionIfNotFound:
            raise BusinessException(ResponseCodes.xdlNotFound)
        return existedXdl

    @staticmethod
    def changeStatus(db, existedXdlList, approve, userId):
        queryList = {
            "_id" : existedXdlList['_id']
        }
        query = {
            "_id" : existedXdlList['xdlId']
        }
        updatedFields = None
        updatedFieldsList = None
        newStatus = None
        if approve:
            updatedFields = {
                '$push' : {
                    "approvedDrugsNames" : existedXdlList['name']
                }
            }
            newStatus = XdlDataAccess.status['approved']
        else:
            updatedFields = {
                '$pull' : {
                    "approvedDrugsNames" : existedXdlList['name']
                }
            }
            newStatus = XdlDataAccess.status['rejected']
        updatedFieldsList = {
            "$set" : {
                "status" : newStatus,
                "statusChangedAt" : datetime.now(tz=timezone.utc),
                "statusChangedBy" : userId
            }
        }
        db.xdl.update_one(query, updatedFields)
        db.xdl_list.update_one(queryList, updatedFieldsList)


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
        items = db.xdl_list.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl_list.count_documents(query)
        return count, items



