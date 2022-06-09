from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
from datetime import timezone,datetime
from src.shared.generalHelper import GeneralHelper

class XdlDataAccess:
    @staticmethod
    def add(db, drugsNames, filePath, xmlList, textList):
        nowDate = datetime.now(tz=timezone.utc)
        i = 0
        while i < len(xmlList):
            xml = xmlList[i]
            text = textList[i]
            name = drugsNames[i]

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
                "updatedAt" : None,
                "deletedAt" : None,
                "approvedAt" : None,
                "rejectedAt" : None,
                "approvedBy" : None,
                "createdBy" : None,
                "rejectedBy" : None
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
            "updatedAt" : 1,
            "approvedAt" : 1,
            "rejectedAt" : 1,
            "approvedBy" : 1,
            "rejectedBy" : 1,
            "createdBy" : 1
        }
        query = {
            "name" : {
                "$regex": criteria,
                "$options": "i"
            },
            "deletedAt" : None
        }
        items = db.xdl_list.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl_list.count_documents(query)
        return {
            "count" : count,
            "items" : items
        }

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
            '_id' : -1
        }
        result = db.xdl.find_one({'_id' : existedXdlList['xdlId']}, projection)
        result ['_id'] =  existedXdlList['_id']
        result ['createdBy'] =  existedXdlList['createdBy']
        result ['approvedAt'] = existedXdlList['approvedAt']
        result ['approvedBy'] = existedXdlList['approvedBy']
        result ['rejectedAt'] = existedXdlList['rejectedAt']
        result ['rejectedBy'] = existedXdlList['rejectedBy']
        return result

    @staticmethod
    def getById(db, id, throwExceptionIfNotFound = True):
        query = {
            "_id" : GeneralHelper.getObjectId(id),
            'deletedAt': None
        }
        existedXdl = db.xdl_list.find_one(query)
        if existedXdl is None and throwExceptionIfNotFound:
            raise BusinessException(ResponseCodes.xdlNotFound)
        return existedXdl

    @staticmethod
    def changeStatus(db, existedXdlList, approve):
        queryList = {
            "_id" : existedXdlList['_id'],
            'deletedAt': None
        }
        query = {
            "_id" : existedXdlList['xdlId'],
            'deletedAt': None
        }
        updatedFields = None
        updatedFieldsList = None
        if approve:
            updatedFields = {
                '$push' : {
                    "approvedDrugsNames" : existedXdlList['name']
                }
            }
            updatedFieldsList =  {
                "$set" : {
                    "approvedAt" : datetime.now(tz=timezone.utc),
                    "rejectedAt" : None
                }
            }
        else:
            updatedFields = {
                '$pull' : {
                    "approvedDrugsNames" : existedXdlList['name']
                }
            }
            updatedFieldsList =  {
                "$set" : {
                    "approvedAt" : None,
                    "rejectedAt" : datetime.now(tz=timezone.utc)
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
            "deletedAt" : None,
            "rejectedAt" : None,
            "approvedAt" : { "$ne" : None }
        }
        projection = {
            "name" : 1,
            "filePath" : 1,
            "createdAt" : 1,
            "approvedAt" : 1,
            "approvedBy" : 1,
            "createdBy" : 1
        }
        items = db.xdl_list.find(query, projection).skip(pageNumber * pageSize).limit(pageSize)
        count = db.xdl_list.count_documents(query)
        return {
            "count" : count,
            "items" : items
        }



