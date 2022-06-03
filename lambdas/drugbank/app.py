import json
from urllib.parse import unquote
from src.drugbank import value_calculator, service, importer
# import requests


def drugbank(event, context):
    drug_name= event['queryStringParameters']['name'] 
    drug_id= event['queryStringParameters']['id']
    props= event['queryStringParameters']['props'] 
    return service.find(drug_name=drug_name, drug_id=drug_id, props=props)

def calculator(event, context):
    return value_calculator.calculator()

def drugbankQuery(event, context):
    query = event['pathParameters']['query']
    page= event['queryStringParameters']['page'] 
    category= event['queryStringParameters']['category'] 
    return service.query(user_query=unquote(query), page=int(page), category=category)

def targetsQuery(event, context):
    query = event['pathParameters']['query']
    return service.query_targets(user_query=unquote(query))

def categoriesQuery(event, context):
    query = event['pathParameters']['query']
    page= event['queryStringParameters']['page'] 
    return service.query_categories(user_query=unquote(query), page=int(page))

def drugsByCategory(event, context):
    category_id = event['pathParameters']['category_id']
    page= event['queryStringParameters']['page'] 
    return service.drugbank_drugs_by_category(category_id, page=int(page))


