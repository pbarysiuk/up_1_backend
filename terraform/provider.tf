provider "aws" {
  region  = "us-east-1"
  profile = "pbarysiuk"
}

terraform {
  required_version = "~> 1.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.8.0"
    }
  }
}