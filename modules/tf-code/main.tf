resource "aws_iam_user" "github_user" {
  name = "version-upgrade1"

  tags = {
    Name = "Github"
  }
}

resource "aws_iam_user_policy" "github_user_policy" {
  name = "test-user-policy"
  user = aws_iam_user.github_user.name

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
