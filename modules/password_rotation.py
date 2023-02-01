#This code can be run as a Lambda function and will automatically check and send emails to IAM users with passwords that are older than 90 days.

import boto3
import re
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Connect to IAM and SES services
    iam = boto3.client('iam')
    ses = boto3.client('ses')

    # List all IAM users
    users = iam.list_users()['Users']

    # Loop through each user
    for user in users:
        username = user['UserName']
        password_policy = iam.get_account_password_policy()
        
        # Check if the user has a password policy
        if password_policy:
            password_last_used = user['PasswordLastUsed'].strftime("%Y-%m-%d")
            current_date = datetime.now().strftime("%Y-%m-%d")
            password_age = (datetime.strptime(current_date, '%Y-%m-%d') - 
                            datetime.strptime(password_last_used, '%Y-%m-%d')).days

            # Check if the password is older than 90 days
            if password_age > 90:
                # Check if the username is a valid email address
                match = re.match(r"[^@]+@[^@]+\.[^@]+", username)
                if match:
                    # Send an email with instructions on how to change password
                    response = ses.send_email(
                        Source='sender@example.com',
                        Destination={'ToAddresses': [username]},
                        Message={
                            'Subject': {
                                'Data': 'AWS IAM Password Change Request'
                            },
                            'Body': {
                                'Text': {
                                    'Data': 'Your AWS IAM password is older than 90 days. Please follow the instructions below to change your password: \n\n1. Log in to the AWS Management Console. \n2. Navigate to the IAM dashboard. \n3. Find your account. \n4. Change your password. \n\nIf you have any questions, please contact support.'
                                }
                            }
                        }
                    )
                    print(f"Sent password change request to {username}")
                else:
                    print(f"Username {username} is not a valid email address")
    return "Password change request emails sent"
