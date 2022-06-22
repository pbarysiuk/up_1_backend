from src.drugbank import service
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    drug_name= LambdaHelper.getQueryStringParam(event, 'name', LambdaHelper.valueTypeString, None)
    drug_id= LambdaHelper.getQueryStringParam(event, 'id', LambdaHelper.valueTypeString, None)
    props= LambdaHelper.getQueryStringParam(event, 'props', LambdaHelper.valueTypeString, None)
    return service.find(drug_name=drug_name, drug_id=drug_id, props=props)
