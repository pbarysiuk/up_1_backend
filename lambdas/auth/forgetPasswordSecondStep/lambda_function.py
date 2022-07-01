from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['forgetPasswordRequestId', 'code', 'password'])
    return BusinessAuth.forgetPasswordSecondStep(requestId=body['forgetPasswordRequestId'], code=body['code'], password=body['password'])


