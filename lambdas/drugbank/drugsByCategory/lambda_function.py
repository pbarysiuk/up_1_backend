from src.drugbank import service
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    category_id = LambdaHelper.getPathParam(event, 'proxy')
    page = LambdaHelper.getQueryStringParam(event, 'page', LambdaHelper.valueTypeInt, 0)
    return service.drugbank_drugs_by_category(category_id, page=page)
