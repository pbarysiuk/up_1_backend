resource "aws_ssm_parameter" "dev_commit_id" {
  name  = "lambda_last_commit_id_dev"
  type  = "String"
  value = "4f56939"
}

resource "aws_ssm_parameter" "stage_commit_id" {
  name  = "lambda_last_commit_id_stage"
  type  = "String"
  value = "4f56939"
}

resource "aws_ssm_parameter" "prod_commit_id" {
  name  = "lambda_last_commit_id_prod"
  type  = "String"
  value = "4f56939"
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