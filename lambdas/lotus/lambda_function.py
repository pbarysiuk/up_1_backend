import json
from os import environ
import re
from bson.objectid import ObjectId
from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper
import pymongo
import traceback
import mysql.connector


def lambda_handler(event, context):
    #return createFullTextIndex(create = False)
    db = event['pathParameters']['proxy']
    user_query = event['queryStringParameters']['query']
    return query(user_query, 0, None)
    pageSize = 100
    if db == 'sql':
        return querySql(user_query, pageSize)
    if db == 'sqlindex':
        return querySqlIndex(user_query, pageSize)
    if db == 'catNew':
        return drugbank_drugs_by_category_new(user_query, 0)
    if db == 'cat':
        return drugbank_drugs_by_category(user_query, 0)
    return queryNoSql(user_query, pageSize)




def queryNoSql(user_query, pageSize):
    try:
        dbConnection = pymongo.MongoClient(environ.get("MONGODB_CONNSTRING"))
        db = dbConnection.drugbank
        #db.xdl.drop()
        #db.xdl_list.drop()
        molecules = db.molecules.find({
            "name" : {
                "$regex": user_query,
                "$options": "i"
            }
        }, {"name" : 1, "smiles" : 1, '_id' : 0}).limit(pageSize)
        result = list(molecules)
        dbConnection.close()
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)



def drugbank_drugs_by_category(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "categories.drugbank_id": category_id
        }
        drugs = db.drugs.find(filter=where_query, projection={'name' : 1}).skip(page * 10).limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
        

def drugbank_drugs_by_category_new(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        category = db.categories_details.find_one({'drugbank_id' : category_id}, {'drugs' : 1})
        where_query = {
            "name": {"$in" : category['drugs']}
        }
        drugs = db.drugs.find(where_query).skip(page * 10).limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)
        
        

def query(user_query: str, page: int, category: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        columns = ["drugbank_id", "name"]
        or_query = {
            '$or': [
                {
                    "clinical_description": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                },
                {
                    "name": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                },
                {
                    "synonyms.synonym": {
                        "$regex": '^' + user_query,
                        "$options": "i"
                    }
                }
            ]
        }
        where_query = {
            "$and": [
                or_query,
            ],
        }
        hint = None
        if category is not None:
            where_query["$and"].append({"categories.drugbank_id": category})
            hint = [('categories.drugbank_id', pymongo.ASCENDING)]
        drugs = None
        drugs = db.drugs_list.find(where_query, hint = hint).skip(page * 10).limit(10)
        count = db.drugs_list.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)

