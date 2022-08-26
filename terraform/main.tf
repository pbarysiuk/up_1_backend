resource "aws_ssm_parameter" "dev_commit_id" {
  name  = "lambda_last_commit_id_dev"
  type  = "String"
  value = "4f56939"
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "stage_commit_id" {
  name  = "lambda_last_commit_id_stage"
  type  = "String"
  value = "4f56939"
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "prod_commit_id" {
  name  = "lambda_last_commit_id_prod"
  type  = "String"
  value = "4f56939"
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_s3_bucket" "dev-lambda" {
  bucket = "prepaire-dev-lambda-artifact-us1"

  tags = {
    Name        = "prepaire-dev-lambda-artifact-us1"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_acl" "dev-lambda" {
  bucket = aws_s3_bucket.dev-lambda.id
  acl    = "private"
}

resource "aws_s3_bucket" "stage-lambda" {
  bucket = "prepaire-stage-lambda-artifact-us1"

  tags = {
    Name        = "prepaire-stage-lambda-artifact-us1"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_acl" "stage-lambda" {
  bucket = aws_s3_bucket.stage-lambda.id
  acl    = "private"
}

resource "aws_s3_bucket" "prod-lambda" {
  bucket = "prepaire-prod-lambda-artifact-us1"

  tags = {
    Name        = "prepaire-prod-lambda-artifact-us1"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_acl" "prod-lambda" {
  bucket = aws_s3_bucket.prod-lambda.id
  acl    = "private"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "auth_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  filename      = "../lambdas/auth_lambda.zip"
  function_name = "prepaire-dev-backend-auth-authorizer"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "authorizer.lambda_function"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("../lambdas/auth_lambda.zip")

  runtime = "python3.9"

  environment {
    variables = {
      env = "dev"
    }
  }
}