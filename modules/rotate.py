import boto3
import json
from datetime import datetime, timedelta
import time

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
    
    # Send email with list of inactive users in CSV format
    if len(inactive_users) > 0:
        inactive_users_csv = 'Username\n'
        for user in inactive_users:
            inactive_users_csv += user + '\n'
        
        message = "The following users haven't logged in for 90 days. Please login to avoid your account being disabled in 14 days:\n{}".format(inactive_users_csv)
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
    
    # Wait for 5 minutes
    wait_time = 300 # 5 minutes in seconds
    time.sleep(wait_time)
    
    # Disable inactive users and send email with list of disabled users
    disabled_users = []
    for user in inactive_users:
        try:
            iam.update_login_profile(
                UserName=user,
                PasswordResetRequired=True
            )
            disabled_users.append(user)
        except Exception as e:
            print(f"Error disabling user {user}: {str(e)}")
    
    if len(disabled_users) > 0:
        disabled_users_csv = 'Username\n'
        for user in disabled_users:
            disabled_users_csv += user + '\n'
        
        message = "The following users have been disabled due to inactivity. Please contact the infrastructure team if you need your account reactivated:\n{}".format(disabled_users_csv)
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
