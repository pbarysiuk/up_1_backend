import boto3
from os import environ
from src.shared.generalHelper import GeneralHelper

class ApiKeysDataAccess:
    @staticmethod
    def create(userId, value, planId):
        if environ.get('LOCAL') is None:
            client = boto3.client('apigateway')
            apiKey = client.create_api_key(name=str(userId), description=value, enabled=True, value=value)
            attachApiKeyToUsagePlan = client.create_usage_plan_key(usagePlanId=planId, keyId=apiKey['id'], keyType='API_KEY')
            return {
                'id' : apiKey['id'],
                'value' : apiKey['value']
            }
        else:
            return {
                'id' : value,
                'value' : value
            }

    @staticmethod
    def delete(id):
        if environ.get('LOCAL') is None:
            client = boto3.client('apigateway')
            client.delete_api_key(apiKey=id)
            return
        else:
            return

    @staticmethod
    def change(id, userId, newValue, newPlanId):
        ApiKeysDataAccess.delete(id)
        return ApiKeysDataAccess.create(userId, newValue, newPlanId)