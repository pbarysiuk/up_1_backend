import json
from urllib.parse import unquote
from src.drugbank import value_calculator, service

def drugbank(event, context):
    drug_name= None
    drug_id= None
    props= None
    if event['queryStringParameters']:
        drug_name= event['queryStringParameters'].get('name') 
        drug_id= event['queryStringParameters'].get('id')
        props= event['queryStringParameters'].get('props') 
    return service.find(drug_name=drug_name, drug_id=drug_id, props=props)

def calculator(event, context):
    return value_calculator.calculator()

def drugbankQuery(event, context):
    query = event['pathParameters']['query']
    page= None
    category= None
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
        category= event['queryStringParameters'].get('category')
    return service.query(user_query=unquote(query), page=int(page), category=category)

def targetsQuery(event, context):
    query = event['pathParameters']['query']
    return service.query_targets(user_query=unquote(query))

def categoriesQuery(event, context):
    query = event['pathParameters']['query']
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
    return service.query_categories(user_query=unquote(query), page=int(page))

def drugsByCategory(event, context):
    category_id = event['pathParameters']['category_id']
    page = 0
    if event['queryStringParameters']:
        page= event['queryStringParameters'].get('page') 
    return service.drugbank_drugs_by_category(category_id, page=int(page))


