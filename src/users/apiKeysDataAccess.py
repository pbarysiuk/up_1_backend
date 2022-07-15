import boto3
from os import environ
from src.shared.generalHelper import GeneralHelper

class ApiKeys:
    @staticmethod
    def create(value, planId):
        if environ.get('LOCAL') is None:
            client = boto3.client('apigateway')
            apiKey = client.create_api_key(name=value, description=value, enabled=True, value=value)
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
    def change(id, newValue, newPlanId):
        ApiKeys.delete(id)
        return ApiKeys.create(newValue, newPlanId)