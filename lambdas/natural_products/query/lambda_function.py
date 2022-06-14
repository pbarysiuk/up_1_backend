from urllib.parse import unquote
from src.natural_products import service

#/natural_products/query/{query}
def lambda_handler(event, context):
    query = unquote(event['pathParameters']['proxy'])
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page')
    return service.query(query=query, page=int(page))    
