import json
import os
import re

from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper

def find(drug_name: str, drug_id: str, props: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        props_list = props and props.split(":") or []
        if not "calculated_properties" in props_list and "toxicity" in props_list:
            props_list.append("calculated_properties")
        query = get_query(drug_id, drug_name)
        drug = db.drugs.find_one(query, props_list)
        if drug is None:
            return {
                "isBase64Encoded": False,
                "statusCode": 404,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": dumps({})
        }
            raise Exception("drug not found")
        return GeneralWrapper.successResult(drug)
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)


def query(user_query: str, page: int, category: str):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        columns = ["drugbank_id", "name", "clinical_description", "chemical_properties", "calculated_properties",
                "experimental_properties", "synonyms", "structured_adverse_effects", "structured_contraindications"]
        or_query = {
            '$or': [
                {
                    "clinical_description": {
                        "$regex": ".*{}.*".format(user_query),
                        "$options": "i"
                    }
                },
                {
                    "calculated_properties": {
                        "$regex": ".*{}.*".format(user_query),
                        "$options": "i"
                    }
                },
                {
                    "chemical_properties": {
                        "$regex": ".*{}.*".format(user_query),
                        "$options": "i"
                    }
                },
                {
                    "name": {
                        "$regex": ".*{}.*".format(user_query),
                        "$options": "i"
                    }
                },
                {
                    "synonyms": {
                        "$regex": ".*{}.*".format(user_query),
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
        if category is not None:
            where_query["$and"].append({"categories.drugbank_id": category})

        drugs = db.drugs.find(where_query, columns) \
            .skip(page * 10) \
            .limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)

def get_query(drug_id, drug_name):
    regx = re.compile("^{}".format(drug_name), re.IGNORECASE)
    ret = {}
    if drug_name:
        ret["name"] = regx
    if drug_id:
        ret["drugbank_id"] = drug_id
    return ret



def document(drug_id: str) -> dict:
    dirname = os.path.dirname(__file__)
    drugbank_dir = os.path.join(dirname, '../../drugbank_docs')
    file_path = os.path.join(drugbank_dir, drug_id + ".json")
    file = open(file_path)
    data = json.load(file)
    file.close()
    return data


def query_targets(user_query: str, page = None, pageSize = None):
    try:
        if not page:
            page = 0
        if not pageSize:
            pageSize = 100
        dbConnection = (Database())
        db = dbConnection.db
        targets = db.targets.find({
            "name": {
                "$regex": ".*{}.*".format(user_query),
                "$options": "i"
            }
        }).skip(page * pageSize).limit(pageSize)
        return GeneralWrapper.successResult(list(targets))
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)


def query_categories(user_query: str, page: int):
    try:    
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "name": {
                "$regex": ".*{}.*".format(user_query),
                "$options": "i"
            }
        }
        categories = db.categories.find(where_query).skip(page * 10) \
            .limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(categories)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)



def drugbank_drugs_by_category(category_id, page):
    try:
        dbConnection = (Database())
        db = dbConnection.db
        where_query = {
            "categories.drugbank_id": category_id
        }
        drugs = db.drugs.find(where_query).skip(page * 10) \
            .limit(10)
        count = db.drugs.count_documents(where_query)
        result = {"count": count, "items": list(drugs)}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        return GeneralWrapper.generalErrorResult(e)
