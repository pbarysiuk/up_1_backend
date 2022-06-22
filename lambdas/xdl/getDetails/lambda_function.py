from src.xdl.business import XdlBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    id = LambdaHelper.getPathParam(event, 'proxy')
    return XdlBusiness.getDetails(id = id)

