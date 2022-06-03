from pymongo import MongoClient
from os import environ
import boto3

class Database:
    def __init__(self):
        connectionString = environ.get("MONGODB_CONNSTRING")
        if not connectionString:
            connectionString = self.__getConnectionStringFromSecret()
        self.client = MongoClient(environ.get("MONGODB_CONNSTRING"))
        self.db = self.client.drugbank

    def __del__(self):
        self.client.close()

    def __getConnectionStringFromSecret(self):
        secret_name = "MONGODB_CONNSTRING"
        region_name = "us-west-2"
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response['SecretString']
        
