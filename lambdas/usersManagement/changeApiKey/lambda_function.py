from src.users.userManagmentBusiness import UserManagmentBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    id = LambdaHelper.getPathParam(event, 'proxy')
    return UserManagmentBusiness.changeApiKeyForUser(token=event.get('headers').get('auth'), userId=id)
