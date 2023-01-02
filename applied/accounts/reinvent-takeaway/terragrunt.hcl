terragrunt_version_constraint = "~> 0.40.0"

remote_state {
  backend = "s3"
  config = {
    bucket         = "reinevent-ci-cd-takeaway"
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
  required_version = "~> 1.3.5" # ~> 1.2.9 , ~> 1.1.3"
}
EOF
}

#generate the backend block via terragrunt in order to keep the S3 backend configuration DRY
#this is just a stub to ensure the backend.tf file exists everywhere to be populated by the terragrunt remote_state configs below
generate "backend" {
  path = "backend.tf"
  if_exists = "overwrite_terragrunt"
  contents = <<EOF
terraform {
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {
  }
}
EOF
}
