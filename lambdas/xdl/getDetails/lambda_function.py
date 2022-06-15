from urllib.parse import unquote
from src.xdl.business import XdlBusiness

def lambda_handler(event, context):
    id = event['pathParameters']['proxy']
    return XdlBusiness.getDetails(id = id)

