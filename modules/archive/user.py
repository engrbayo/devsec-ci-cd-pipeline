import boto3
import json
import time
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Connect to AWS services
    iam = boto3.client('iam')
    ses = boto3.client('ses')

    # Calculate date 90 days ago
    inactive_cutoff = datetime.today() - timedelta(days=90)

    # Get list of all users in AWS account
    all_users = iam.list_users()['Users']

    # Identify inactive users who haven't logged in for 90 days
    inactive_users = []
    for user in all_users:
        password_last_used = iam.get_user(UserName=user['UserName'])['User'].get('PasswordLastUsed')
        if password_last_used is None:
            inactive_users.append(user['UserName'])
        elif password_last_used < inactive_cutoff:
            inactive_users.append(user['UserName'])

    # Send email with list of inactive users
    if len(inactive_users) > 0:
        inactive_users_json = json.dumps(inactive_users)
        message = "The following users haven't logged in 90 days, please login to avoid your account being disabled in 14 days: {}".format(inactive_users_json)
        ses.send_email(
            Source='darekorex143@gmail.com',
            Destination={
                'ToAddresses': ['darekorex143@gmail.com']
            },
            Message={
                'Subject': {'Data': 'Inactive AWS Users'},
                'Body': {'Text': {'Data': message}}
            }
        )

    # Wait for 3 minutes
    time.sleep(180)

    # Disable inactive users and send email with list of disabled users
    disabled_users = []
    for user in inactive_users:
        try:
            iam.update_login_profile(
                UserName=user,
                PasswordResetRequired=True
            )
            disabled_users.append(user)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                continue
            else:
                raise

    if len(disabled_users) > 0:
        disabled_users_json = json.dumps(disabled_users)
        message = "The following users have been disabled due to inactivity, please contact the infrastructure team if you need your account reactivated: {}".format(disabled_users_json)
        ses.send_email(
            Source='darekorex143@gmail.com',
            Destination={
                'ToAddresses': ['darekorex143@gmail.com']
            },
            Message={
                'Subject': {'Data': 'Disabled AWS Users'},
                'Body': {'Text': {'Data': message}}
            }
        )
