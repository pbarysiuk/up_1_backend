from src.users.authBusiness import AuthBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['thirdPartyType', 'thirdPartyToken'])
    return AuthBusiness.loginWithThirdParty(thrirdPartyType=body['thirdPartyType'], thirdPartyToken=body['thirdPartyToken'])


