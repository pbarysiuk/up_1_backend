from urllib.parse import unquote
from src.xdl.business import XdlBusiness

def lambda_handler(event, context):
    approve = event['body'].get('approve')
    id = event['pathParameters']['proxy']
    return XdlBusiness.changeStatus(id= id, status=approve)  
