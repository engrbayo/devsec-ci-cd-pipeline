from datetime import datetime, timedelta
import boto3

def lambda_handler(event, context):
    # Connect to IAM client
    iam = boto3.client('iam')
    
    # Connect to SES client
    ses = boto3.client('ses')
    
    # Get all IAM users
    users = iam.list_users()
    
    # Loop through each user
    for user in users['Users']:
        username = user['UserName']
        # Check if the user has access keys
        keys = iam.list_access_keys(UserName=username)
        if keys['AccessKeyMetadata']:
            for key in keys['AccessKeyMetadata']:
                # Check the age of the keys
                age = datetime.now(datetime.timezone.utc) - key['CreateDate']
                if age > timedelta(days=90):
                    # If the username is an email address, send message to rotate keys
                    if '@' in username:
                        to_address = username
                        subject = 'Rotate Your AWS IAM Access Key'
                        message = f"Your AWS IAM access key has been active for more than 90 days.\n\n"
                        message += "Instructions on how to rotate your key:\n"
                        message += "1. Log in to the AWS Management Console\n"
                        message += "2. Go to the IAM console\n"
                        message += "3. Click on the Users link\n"
                        message += f"4. Click on the user name: {username}\n"
                        message += "5. Click on the Security credentials tab\n"
                        message += "6. Click on the Manage access keys button\n"
                        message += "7. Click on the Deactivate link next to the old key\n"
                        message += "8. Click on the Create access key button\n"
                        message += "9. Click on the Download key file button to download the new key\n"
                        message += "10. Store the new key in a secure location\n"
                        message += "11. Update your scripts or applications with the new key\n"
                        message += "12. Delete the old key\n\n"
                        message += "For more information, please refer to the AWS documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_RotateAccessKey"
                        ses.send_email(
                            Source='Sender Email Address',
                            Destination={
                                'ToAddresses': [
                                    to_address
                                ]
                            },
                            Message={
                                'Subject': {
                                    'Data': subject
                                },
                                'Body': {
                                    'Text': {
                                        'Data': message
                                    }
                                }
                            }
                        )
    return 'Check complete'
