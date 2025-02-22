variable "region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-central-1"
}

variable "deploy_role_name" {
  description = "The name of the IAM role used for deployments"
  type        = string
  default     = "deployment_role"
}

variable "allowed_principals" {
  description = "List of IAM ARNs or AWS Account IDs allowed to assume the role"
  type        = list(string)
  default     = [
    # rashmi-carol-dsouza
    "arn:aws:iam::477896369815:root"
  ]
}
