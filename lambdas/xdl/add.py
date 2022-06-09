from urllib.parse import unquote
from src.xdl.business import XdlBusiness

def lambda_handler(event, context):
    drugsNames = event['body'].get('drugsNames')
    filePath = event['body'].get('filePath')
    xml = event['body'].get('xml')
    text = event['body'].get('text')
    return XdlBusiness.add(drugsNames = drugsNames, filePath=filePath, xml = xml, text=text)   
