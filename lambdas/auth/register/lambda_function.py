from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['name', 'email', 'password', 'image'])
    return AuthBusiness.register(name=body["name"], email=body["email"], password = body["password"], image=body['image'])


