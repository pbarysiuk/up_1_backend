from urllib.parse import unquote
from src.users.userManagmentBusiness import UserManagmentBusiness
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    query = LambdaHelper.getQueryStringParam(event, 'query', LambdaHelper.valueTypeString, '')
    query = unquote(query)
    page = LambdaHelper.getQueryStringParam(event, 'page', LambdaHelper.valueTypeInt, 0)
    pageSize = LambdaHelper.getQueryStringParam(event, 'pageSize', LambdaHelper.valueTypeInt, 10)
    return UserManagmentBusiness.getUsersList(token=event.get('headers').get('auth'), criteria=query, pageNumber=page, pageSize=pageSize)

