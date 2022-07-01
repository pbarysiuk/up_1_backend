from os import environ
#import boto3
#from botocore.exceptions import ClientError
#from src.shared.lambdaHelper import LambdaHelper
import smtplib
from email.message import EmailMessage
import traceback

class Email:
    '''
    @staticmethod
    def __sendEmail(toEmails, title, content):
        sender = LambdaHelper.getValueFromParameterStore(envKey='PS_EMAIL_SENDER', defaultEnvKey='EMAIL_SENDER')
        #awsRegion=environ.get('EMAIL_AWS_REGION')
        charset = "utf-8"
        #awsCred = {
        #    "aws_access_key_id":environ.get('AWS_ACCESS_KEY'),
        #    "aws_secret_access_key":environ.get('AWS_SECRET_KEY') 
        #}
        #client = boto3.client('ses',**awsCred, region_name=awsRegion)
        try:
            client = boto3.client('ses')
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
        #except NoRegionError as e:
        #    print(e.response['Error']['Message'])
        except ClientError as e:
            print(e.response['Error']['Message'])
        except Exception as e:
            print(e)
        #else:
        #    print("Email sent! Message ID:"),
        #    print(response['MessageId'])
        return
    '''

    @staticmethod
    def __sendEmail(toEmails, title, content):
        try:
            msg = EmailMessage()
            msg['Subject'] = title
            msg['From'] = environ.get('MAIL_USER')
            msg['To'] = ', '.join(toEmails)
            msg.set_content(content)
            server = smtplib.SMTP(environ.get('MAIL_HOST'), environ.get('MAIL_PORT'))
            server.starttls()
            server.login(environ.get('MAIL_USER'), environ.get('MAIL_PASS'))  # user & password
            server.send_message(msg)
            server.quit()
        except Exception as e:
            traceback.print_exc(e)


    @staticmethod
    def sendForgetPasswordEmail(toEmail, forgetPasswordCode):
        title = "Prepaire forget password"
        content = "Your forget password code is: " + str(forgetPasswordCode)
        return Email.__sendEmail([toEmail], title, content)

    @staticmethod
    def sendVerificationEmail(toEmail, verificationCode):
        title = "Prepaire verification email"
        content = "Your verification code is: " + str(verificationCode)
        return Email.__sendEmail([toEmail], title, content)

    @staticmethod
    def sendCreateUserEmail(toEmail, password):
        title = "Prepaire account"
        content = "You can login to your Prepaire account using the following credentials:\nEmail: " + toEmail + "\nPassword: " + password + "\nPlease consider changing password after login"
        return Email.__sendEmail([toEmail], title, content)