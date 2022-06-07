from os import environ
import boto3
from botocore.exceptions import ClientError

class Email:
    @staticmethod
    def __sendEmail(toEmails, title, content):
        sender = environ.get('EMAIL_SENDER')
        awsRegion=environ.get('EMAIL_AWS_REGION')
        charset = "utf-8"
        awsCred = {
            "aws_access_key_id":environ.get('AWS_ACCESS_KEY'),
            "aws_secret_access_key":environ.get('AWS_SECRET_KEY') 
        }
        client = boto3.client('ses',**awsCred, region_name=awsRegion)
        try:
            response = client.send_email(
                Destination={
                    "ToAddresses": toEmails,
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": charset,
                            "Data": content,
                        }
                    },
                    "Subject": {
                        "Charset": charset,
                        "Data": title,
                    },
                },
                Source=sender,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        return


    @staticmethod
    def sendForgetPasswordEmail(toEmail, forgetPasswordCode):
        title = "Prepaire forget password"
        content = "Your forget password code is: " + str(forgetPasswordCode)
        return Email.__sendEmail([toEmail], title, content)

    @staticmethod
    def sendCreateUserEmail(toEmail, password):
        title = "Prepaire account"
        content = "You can login to your Prepaire account using the following credentials:\nEmail: " + toEmail + "\nPassword: " + password + "\nPlease consider changing password after login"
        return Email.__sendEmail([toEmail], title, content)