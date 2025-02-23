output "invoke_url" {
  description = "The invoke URL for the API endpoint"
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.region}.amazonaws.com/${var.stage_name}/generated-ads"
}
