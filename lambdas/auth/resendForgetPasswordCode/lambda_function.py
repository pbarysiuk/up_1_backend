from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['forgetPasswordRequestId'])
    return AuthBusiness.resendForgetPasswordCode(requestId=body['forgetPasswordRequestId'])


