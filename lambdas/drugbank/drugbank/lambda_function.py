from src.drugbank import service

def lambda_handler(event, context):
    drug_name= None
    drug_id= None
    props= None
    if event['queryStringParameters']:
        drug_name= event['queryStringParameters'].get('name') 
        drug_id= event['queryStringParameters'].get('id')
        props= event['queryStringParameters'].get('props') 
    return service.find(drug_name=drug_name, drug_id=drug_id, props=props)
