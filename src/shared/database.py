from pymongo import MongoClient
from os import environ
import boto3
import traceback

class Database:
    def __init__(self):
        connectionString = None
        try:
            connectionString = self.__getConnectionStringFromParameterStore()
        except Exception as e:
            traceback.print_exc()
            connectionString = None
        if connectionString is None:
            connectionString = environ.get("MONGODB_CONNSTRING")
        self.client = MongoClient(connectionString)
        self.db = self.client.drugbank

    def __del__(self):
        self.client.close()

    def __getConnectionStringFromParameterStore(self):
        ssm = boto3.client('ssm')
        parameterName = environ.get("PARAM_STORE_MONGODB")
        parameter = ssm.get_parameter(Name=parameterName, WithDecryption=True)
        return (parameter['Parameter']['Value'])
        
