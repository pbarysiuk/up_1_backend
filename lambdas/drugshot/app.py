import json

# import requests

from src.drughshot import service

#/drugshot/api/search', methods=['POST']
def search(event, context):
    return service.search(event['body'])    


#/drugshot/api/associate', methods=['POST']
def associate(event, context):
    return service.associate(event['body'])  
