from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['email', 'password'])
    return BusinessAuth.login(email=body['email'], password=body['password'])


