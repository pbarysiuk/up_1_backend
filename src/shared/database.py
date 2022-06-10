from pymongo import MongoClient
from os import environ
import boto3

class Database:
    def __init__(self):
        connectionString = environ.get("MONGODB_CONNSTRING")
        if not connectionString:
            connectionString = self.__getConnectionStringFromParameterStore()
        self.client = MongoClient(connectionString)
        self.db = self.client.drugbank

    def __del__(self):
        self.client.close()

    def __getConnectionStringFromParameterStore(self):
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='devPrepaireDocumentDB', WithDecryption=True)
        return (parameter['Parameter']['Value'])
        
