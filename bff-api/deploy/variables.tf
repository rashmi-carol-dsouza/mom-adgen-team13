variable "region" {
  description = "AWS region to deploy in"
  type        = string
  default     = "eu-central-1"
}

variable "instance_name" {
  description = "Name tag for the EC2 instance"
  type        = string
  default     = "bff-api"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID to use for the EC2 instance (default is Amazon Linux 2)"
  type        = string
  default     = "ami-06ee6255945a96aba"
}

variable "vpc_id" {
  description = "VPC ID where the instance will be launched"
  type        = string
  default = "vpc-c02e81aa"
}

variable "subnet_id" {
  description = "Subnet ID within the VPC to launch the instance"
  type        = string
  default = "subnet-23e77149"
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the instance (HTTP on port 5000 and SSH on port 22)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "flask_app_repo_url" {
  description = "Git repository URL containing your Flask app code"
  type        = string
  default = "https://github.com/rashmi-carol-dsouza/mom-adgen-team13.git"
}

variable "tags" {
  description = "A map of tags to add to resources"
  type        = map(string)
  default     = {
    Project       = "mom-2025"
    Component     = "bff-api"
  }
}
