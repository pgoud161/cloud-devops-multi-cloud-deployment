################################################################################
# Terraform AWS Variables
################################################################################

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (dev / staging / production)"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}

variable "project_name" {
  description = "Unique project prefix used for all resource names"
  type        = string
  default     = "cloud-devops"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  description = "Availability zones to use for subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "admin_cidr" {
  description = "Your IP CIDR allowed for SSH access to EC2"
  type        = string
  default     = "0.0.0.0/0"  # Restrict this in production
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ec2_public_key" {
  description = "SSH public key for EC2 key pair"
  type        = string
  sensitive   = true
}

variable "github_repo" {
  description = "GitHub org/repo path used to pull the container image"
  type        = string
  default     = "your-github-username/cloud-devops-multi-cloud-deployment"
}
