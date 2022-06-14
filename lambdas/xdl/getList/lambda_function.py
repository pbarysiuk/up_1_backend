from urllib.parse import unquote
from src.xdl.business import XdlBusiness

#/natural_products/query/{query}
def lambda_handler(event, context):
    query = event['queryStringParameters'].get('query')
    if query is None:
        query = ''
    query = unquote(query)
    page = int(event['queryStringParameters'].get('page'))
    pageSize = int(event['queryStringParameters'].get('pageSize'))
    return XdlBusiness.getList(query=query, pageNumber=page, pageSize=pageSize)