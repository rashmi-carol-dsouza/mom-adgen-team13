variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "handler" {
  description = "Lambda handler (e.g., file.function)"
  type        = string
}

variable "runtime" {
  description = "Lambda runtime (e.g., python3.8)"
  type        = string
}

variable "lambda_source_dir" {
  description = "Path to the Lambda function source directory"
  type        = string
}

variable "tags" {
  description = "A map of tags to add to resources"
  type        = map(string)
}
