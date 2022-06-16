from urllib.parse import unquote
from src.xdl.business import XdlBusiness
from json import loads

def lambda_handler(event, context):
    body = loads(event['body'])
    approve = body.get('approve')
    name = body.get('name')
    id = event['pathParameters']['proxy']
    return XdlBusiness.changeStatus(id= id, status=approve, name=name)  
