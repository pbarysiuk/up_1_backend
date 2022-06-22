from urllib.parse import unquote
from src.xdl.business import XdlBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    query = LambdaHelper.getQueryStringParam(event, 'query', LambdaHelper.valueTypeString, '')
    query = unquote(query)
    page = LambdaHelper.getQueryStringParam(event, 'page', LambdaHelper.valueTypeInt, 0)
    pageSize = LambdaHelper.getQueryStringParam(event, 'pageSize', LambdaHelper.valueTypeInt, 10)
    return XdlBusiness.search(query=query, pageNumber=page, pageSize=pageSize)

