from src.xdl.business import XdlBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    id = LambdaHelper.getPathParam(event, 'proxy')
    body = LambdaHelper.getBodyParams(event, ['approve', 'name', 'title'])
    return XdlBusiness.changeStatus(id= id, status=body['approve'], name=body['name'], title=body['title'])  
