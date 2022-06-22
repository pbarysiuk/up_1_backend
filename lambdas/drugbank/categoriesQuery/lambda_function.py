from urllib.parse import unquote
from src.drugbank import  service

def lambda_handler(event, context):
    query = event['pathParameters']['proxy']
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
    return service.query_categories(user_query=unquote(query), page=int(page))
