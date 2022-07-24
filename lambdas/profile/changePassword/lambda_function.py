from src.users.profileBusiness import ProfileBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['newPassword'])
    return ProfileBusiness.changePassword(token=event.get('headers').get('auth'), newPassword=body["newPassword"])
