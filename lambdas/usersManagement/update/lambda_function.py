from src.users.userManagmentBusiness import UserManagmentBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    id = LambdaHelper.getPathParam(event, 'proxy')
    body = LambdaHelper.getBodyParams(event, ['name', 'email', 'role', 'image'])
    return UserManagmentBusiness.updateUser(token=event.get('headers').get('auth'), userId=id, name=body["name"], email=body["email"], role = body["role"], image = body['image'])
