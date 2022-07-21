import json
from os import environ
import re
from unittest import result
from bson.objectid import ObjectId
from bson.json_util import dumps
from src.shared.database import Database
from src.shared.generalWrapper import GeneralWrapper
import pymongo
import traceback
import mysql.connector
import numpy as np
from src.shared.generalHelper import GeneralHelper
from src.users.apiKeysDataAccess import ApiKeysDataAccess
from json import loads


planId = ''


def lambda_handler(event, context):
    guid = GeneralHelper.generateGUID()
    result = ApiKeysDataAccess.create(guid, planId)
    return GeneralWrapper.successResult(result)
    

def create():
    guid = GeneralHelper.generateGUID()
    result = ApiKeysDataAccess.create(guid, planId)
    return GeneralWrapper.successResult(result)

def change(id):
    guid = GeneralHelper.generateGUID()
    result = ApiKeysDataAccess.change(id, guid, planId)
    return GeneralWrapper.successResult(result)

def delete(id):
    result = ApiKeysDataAccess.delete(id)
    return GeneralWrapper.successResult(result)