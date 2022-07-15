from src.drugbank import  service
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['drug', 'weight', 'age', 'gender', 'geo'])
    return service.calculateMaintenanceDosage(body['drug'], body['weight'], body['age'], body['gender'], body['geo'])
