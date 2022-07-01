from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['email'])
    return BusinessAuth.forgetPasswordFirstStep(email=body['email'])


