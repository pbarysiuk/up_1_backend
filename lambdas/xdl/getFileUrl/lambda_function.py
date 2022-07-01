import json
import logging
import boto3
from botocore.exceptions import ClientError
from os import environ
from src.shared.generalWrapper import GeneralWrapper
from src.shared.exceptions.businessException import BusinessException
from src.shared.exceptions.responseCodes import ResponseCodes
import traceback
from src.shared.lambdaHelper import LambdaHelper


def lambda_handler(event, context):
    try:
        filePath = LambdaHelper.getPathParam(event, 'proxy')
        url = create_presigned_url(bucket_name =  environ.get("BUCKET_NAME"),object_name = filePath)
        if url is None:
            raise BusinessException(ResponseCodes.fileNotFound)
        result = {'url' : url}
        return GeneralWrapper.successResult(result)
    except Exception as e:
        traceback.print_exc()
        return GeneralWrapper.generalErrorResult(e)


def create_presigned_url(bucket_name, object_name, expiration=120):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

