import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    iam = boto3.client('iam')

    # Get list of IAM users
    users = iam.list_users()
    expired_keys_users = []

    for user in users['Users']:
        user_name = user['UserName']

        # Get access keys for each user
        access_keys = iam.list_access_keys(UserName=user_name)

        # Check if the 'Email' key is present in the user dictionary
        if 'Email' in user:
            email = user['Email']
        else:
            email = None

        # Loop through each access key
        for access_key in access_keys['AccessKeyMetadata']:
            access_key_id = access_key['AccessKeyId']
            created_date = access_key['CreateDate']

            # Check if access key is older than 180 days
            now = datetime.now()
            key_age = now - created_date.replace(tzinfo=None)
            if key_age > timedelta(days=180):
                # Add user to list with expired access key
                expired_keys_users.append({
                    'user_name': user_name,
                    'email': email,
                    'access_key_id': access_key_id
                })

    # Send SES message to users with expired access key
    ses = boto3.client('ses')
    for user in expired_keys_users:
        user_name = user['user_name']
        email = user['email']
        access_key_id = user['access_key_id']

        message = f"IAM user access key with ID: {access_key_id} for user {user_name} is older than 180 days and needs to be rotated."
        ses.send_email(
            Source='oodo@ptc.com',
            Destination={
                'ToAddresses': ['oodo@ptc.com', 'darekorex143@gmail.com']
            },
            Message={
                'Subject': {
                    'Data': 'IAM User Access Key Expiration Notification'
                },
                'Body': {
                    'Text': {
                        'Data': message
                    }
                }
            }
        )




# Load the Azure.Identity module
Import-Module Azure.Identity

# Get the tenant ID and client ID of the service principal
$tenantId = Read-Host -Prompt "Enter Azure AD tenant ID"
$clientId = Read-Host -Prompt "Enter client ID of the service principal"

# Connect to Azure AD using the service principal
Connect-AzureAD -TenantId $tenantId -ApplicationId $clientId -CertificateThumbprint <Thumbprint>

# Get list of Azure AD users
$users = Get-AzureADUser

# Loop through each user
foreach ($user in $users) {
    # Get the last login time for the user
    $lastLoginTime = Get-AzureADAuditSignInLogs -Filter "userDisplayName eq '$($user.DisplayName)'" | Select-Object -First 1

    # Check if the last login time is longer than 180 days ago
    $cutoffTime = (Get-Date).AddDays(-180)
    if ($lastLoginTime.CreationTime -lt $cutoffTime) {
        # Disable the user if the last login was more than 180 days ago
        Set-AzureADUser -ObjectId $user.ObjectId -AccountEnabled $false
    }
}
