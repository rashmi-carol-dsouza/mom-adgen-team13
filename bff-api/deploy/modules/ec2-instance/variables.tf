variable "instance_name" {
  description = "Name tag for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the instance"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the instance will be deployed"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID where the instance will be launched"
  type        = string
}

variable "allowed_cidr_blocks" {
  description = "Allowed CIDR blocks for security group ingress"
  type        = list(string)
}

variable "flask_app_repo_url" {
  description = "Git repository URL for your Flask app"
  type        = string
}
