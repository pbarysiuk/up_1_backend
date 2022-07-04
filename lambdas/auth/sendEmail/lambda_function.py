from src.shared.emails import Email
import json
import traceback

def lambda_handler(event, context):
    if event.get('Records') is None:
        return {
            'statusCode': 200,
            'body': json.dumps('1')
        }
    for r in event.get('Records'):
        try:
            content = r['body']
            title = r['messageAttributes']['title']['stringValue']
            toEmail = r['messageAttributes']['toEmail']['stringValue']
            Email.sendEmailSMTP([toEmail], title, content)
        except Exception as e:
            traceback.print_exc(e)
    return {
        'statusCode': 200,
        'body': json.dumps('1')
    }


