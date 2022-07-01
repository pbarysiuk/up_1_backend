from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['email', 'password', 'code'])
    return BusinessAuth.verify(email=body['email'], code=body['code'], password=body['password'])


