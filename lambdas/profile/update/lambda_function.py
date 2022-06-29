from src.users.profileBusiness import ProfileBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['name', 'email', 'image'])
    return ProfileBusiness.updateProfile(token=event.get('headers').get('auth'),  name=body["name"], email=body["email"], image = body['image'])
