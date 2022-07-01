from urllib.parse import unquote
from src.drugbank import  service
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    query = LambdaHelper.getPathParam(event, 'proxy')
    page = LambdaHelper.getQueryStringParam(event, 'page', LambdaHelper.valueTypeInt, 0)
    return service.query_categories(user_query=unquote(query), page=page)
