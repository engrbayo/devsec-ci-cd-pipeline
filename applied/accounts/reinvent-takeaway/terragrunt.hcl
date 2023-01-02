terragrunt_version_constraint = "~> 0.36.2"

remote_state {
  backend = "s3"
  config = {
    bucket         = "reinevent-ci/cd-takeaway"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "my-lock-table"
  }
}


#generate the versions block via terragrunt in order to keep the terraform & provider version configuration DRY
generate "versions" {
  path = "versions.tf"
  if_exists = "overwrite" #had to overwrite existing since there is a dummy file there in order to enable the "discovery" of the folder
  contents = <<EOF
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.30.0" # ~> 4.30.0 , ">=3.0.0, < 5.0.0"
    }
  }
  required_version = "~> 1.2.9" # ~> 1.2.9 , ~> 1.1.3"
}
EOF
}