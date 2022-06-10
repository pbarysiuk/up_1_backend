from urllib.parse import unquote
from src.xdl.business import XdlBusiness
from json import loads

def lambda_handler(event, context):
    body = loads(event['body'])
    drugs = body.get('drugs')
    filePath = body.get('filePath')
    return XdlBusiness.add(drugs = drugs, filePath = filePath)   
