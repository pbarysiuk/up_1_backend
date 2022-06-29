from pymongo import MongoClient
from os import environ
from src.shared.lambdaHelper import LambdaHelper

class Database:
    def __init__(self):
        connectionString = LambdaHelper.getValueFromParameterStore(envKey= "PARAM_STORE_MONGODB", defaultEnvKey="MONGODB_CONNSTRING")
        self.client = MongoClient(connectionString)
        self.db = self.client.drugbank

    def __del__(self):
        self.client.close()


        
