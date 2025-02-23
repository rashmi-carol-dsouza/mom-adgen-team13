output "deploy_role_arn" {
  description = "ARN of the deployment IAM role"
  value       = aws_iam_role.deploy_role.arn
}
