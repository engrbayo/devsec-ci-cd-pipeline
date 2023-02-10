#

import boto3
import json
from datetime import datetime, timedelta
from teams import Teams

# Connect to AWS IAM
client = boto3.client('iam')

# Set time threshold for inactive roles (180 days ago)
time_threshold = datetime.now() - timedelta(days=180)

# Get list of IAM roles
roles = client.list_roles()

# Initialize Teams client
teams = Teams(teams_webhook_url1, teams_webhook_url2)

# Iterate through roles and check if they have not been used in the last 180 days
for role in roles['Roles']:
    if 'LastUsedDate' in role:
        last_used = role['LastUsedDate'].replace(tzinfo=None)
        if last_used < time_threshold:
            # Get the policy attached to the role
            policy = client.get_role_policy(RoleName=role['RoleName'], PolicyName='default')
            policy_json = json.dumps(policy['PolicyDocument'], indent=4)
            # Send the role and policy information to Teams
            teams.send_message(f"Role: {role['RoleName']}\n\nPolicy:\n{policy_json}")