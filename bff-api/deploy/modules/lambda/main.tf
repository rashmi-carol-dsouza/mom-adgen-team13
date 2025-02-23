resource "aws_iam_role" "lambda_exec" {
  name = "${var.function_name}_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "lambda_layer_access" {
  name        = "${var.function_name}_layer_access"
  description = "Allows Lambda function to access public layers"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "lambda:GetLayerVersion"
        Resource = "arn:aws:lambda:eu-central-1:898466741470:layer:psycopg2-py38:1"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_layer_access_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_layer_access.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.lambda_source_dir
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  handler          = var.handler
  runtime          = var.runtime
  role             = aws_iam_role.lambda_exec.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  layers = [
    "arn:aws:lambda:eu-central-1:898466741470:layer:psycopg2-py38:1"
  ]
}
