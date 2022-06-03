import json

# import requests

from src.lotus import service

#/lotus/query/<string:query>
def lambda_handler(event, context):
    query = event['pathParameters']['query']
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page')
    return service.query(query=query, page=int(page))    
