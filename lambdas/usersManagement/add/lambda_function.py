from src.users.userManagmentBusiness import UserManagmentBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['name', 'email', 'role', 'image'])
    return UserManagmentBusiness.addUser(token=event.get('headers').get('auth'), name=body["name"], email=body["email"], role = body["role"], image=body['image'])


