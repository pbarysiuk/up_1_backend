from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['password'])
    return AuthBusiness.resetPasswordFirstTime(resetPasswordToken=event.get('headers').get('auth'), password=body["password"])
