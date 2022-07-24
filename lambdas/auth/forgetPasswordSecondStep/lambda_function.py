from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['forgetPasswordRequestId', 'code', 'password'])
    return AuthBusiness.forgetPasswordSecondStep(requestId=body['forgetPasswordRequestId'], code=body['code'], password=body['password'])


