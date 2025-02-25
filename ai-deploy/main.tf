provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "mp3_storage" {
  bucket = "event-advert-mp3-storage"
  force_destroy = true
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_execution_role" 
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_execution_policy"
  description = "IAM policy for AWS Lambda execution"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:eu-central-1:*:*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = [
          "arn:aws:s3:::event-advert-mp3-storage",
          "arn:aws:s3:::event-advert-mp3-storage/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}


resource "aws_lambda_function" "event_advert_lambda" {
  function_name    = "event-advert-api"
  runtime         = "python3.11"  
  handler         = "lambda_function.lambda_handler"  
  role            = aws_iam_role.lambda_exec_role.arn
  timeout         = 30
  memory_size     = 1024

  filename        = "lambda_function.zip"  
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      S3_BUCKET_NAME = "event-advert-mp3-storage"
    }
  }
}

resource "aws_api_gateway_rest_api" "event_api" {
  name        = "EventAdvertAPI"
  description = "API Gateway for event advertisements"
}

resource "aws_api_gateway_resource" "generate_advert" {
  rest_api_id = aws_api_gateway_rest_api.event_api.id
  parent_id   = aws_api_gateway_rest_api.event_api.root_resource_id
  path_part   = "generate-advert"
}

resource "aws_api_gateway_method" "post_generate_advert" {
  rest_api_id   = aws_api_gateway_rest_api.event_api.id
  resource_id   = aws_api_gateway_resource.generate_advert.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.event_api.id
  resource_id = aws_api_gateway_resource.generate_advert.id
  http_method = aws_api_gateway_method.post_generate_advert.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.event_advert_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.event_advert_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.event_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "event_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.event_api.id
  depends_on  = [aws_api_gateway_integration.lambda_integration]
}

resource "aws_api_gateway_stage" "prod_stage" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.event_api.id
  deployment_id = aws_api_gateway_deployment.event_api_deployment.id
}

output "api_gateway_url" {
  value = aws_api_gateway_deployment.event_api_deployment.invoke_url
}
