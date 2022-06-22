from urllib.parse import unquote
from src.drugbank import service

def lambda_handler(event, context):
    query = event['pathParameters']['proxy']
    page= None
    category= None
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
        category= event['queryStringParameters'].get('category')
    return service.query(user_query=unquote(query), page=int(page), category=category)
