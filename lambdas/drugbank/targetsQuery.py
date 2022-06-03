from urllib.parse import unquote
from src.drugbank import  service

def lambda_handler(event, context):
    query = event['pathParameters']['proxy']
    return service.query_targets(user_query=unquote(query))