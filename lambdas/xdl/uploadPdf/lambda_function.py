import json
import base64
import boto3
import uuid
from src.shared.generalWrapper import GeneralWrapper
import traceback
import os

def lambda_handler(event, context):
    try:
        content = base64.b64decode(event['body'])
        BUCKET_NAME = os.environ.get("BUCKET_NAME")
        file_path = str(uuid.uuid4()) + '.pdf'
        s3 = boto3.client('s3')
        s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=content)
        #url = s3.generate_presigned_url(ClientMethod = 'put_object', Params = { 'Bucket': BUCKET_NAME, 'Key': file_path })
        #url = url[0 : url.index('?')]
        result = {'file_path' : file_path}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e) 
