from src.drugbank import service

def lambda_handler(event, context):
    category_id = event['pathParameters']['category_id']
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
    return service.drugbank_drugs_by_category(category_id, page=int(page))