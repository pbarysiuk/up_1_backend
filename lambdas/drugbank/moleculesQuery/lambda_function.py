from urllib.parse import unquote
from src.drugbank import  service
from src.shared.lambdaHelper import LambdaHelper

def lambda_handler(event, context):
    query = LambdaHelper.getPathParam(event, 'proxy')
    return service.moleculeQuery(user_query=unquote(query))

