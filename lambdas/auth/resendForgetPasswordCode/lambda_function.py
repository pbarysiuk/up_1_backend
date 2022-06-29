from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['forgetPasswordRequestId'])
    return BusinessAuth.resendForgetPasswordCode(requestId=body['forgetPasswordRequestId'])


