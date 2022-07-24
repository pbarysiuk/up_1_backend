from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['email'])
    return AuthBusiness.forgetPasswordFirstStep(email=body['email'])


