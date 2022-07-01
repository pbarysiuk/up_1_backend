from src.users.authBusiness import BusinessAuth
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    return BusinessAuth.refreshToken(refreshToken=event.get('headers').get('auth'))


