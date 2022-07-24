from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    return AuthBusiness.refreshToken(refreshToken=event.get('headers').get('auth'))


