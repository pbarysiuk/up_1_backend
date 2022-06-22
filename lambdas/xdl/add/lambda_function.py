from src.xdl.business import XdlBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    body = LambdaHelper.getBodyParams(event, ['drugs', 'filePath'])
    return XdlBusiness.add(drugs = body['drugs'], filePath = body['filePath'])   

