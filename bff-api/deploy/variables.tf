variable "region" {
  description = "AWS region"
  default     = "eu-central-1"
}

variable "stage_name" {
  description = "API Gateway stage name"
  default     = "dev"
}

variable "tags" {
  description = "A map of tags to add to resources"
  type        = map(string)
  default     = {
    Project       = "mom-2025"
    Component     = "bff-api"
  }
}
