from urllib.parse import unquote
from src.natural_products import service
from src.shared.lambdaHelper import LambdaHelper

#/natural_products/query/{query}
def lambda_handler(event, context):
    query = LambdaHelper.getPathParam(event, 'proxy')
    page = LambdaHelper.getQueryStringParam(event, 'page', LambdaHelper.valueTypeInt, 0)
    return service.query(query=unquote(query), page=page)  

