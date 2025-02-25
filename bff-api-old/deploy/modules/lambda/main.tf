resource "aws_iam_role" "lambda_exec" {
  name = "${var.function_name}_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Allow Lambda to Assume Role
resource "aws_iam_policy" "lambda_assume_role" {
  name        = "${var.function_name}_assume_role"
  description = "Allows Lambda function to assume IAM role"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "iam:PassRole",
        Resource = aws_iam_role.lambda_exec.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_assume_role_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_assume_role.arn
}

# Full Lambda Execution Permissions
resource "aws_iam_policy" "lambda_permissions" {
  name        = "${var.function_name}_lambda_permissions"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = "*",
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = "iam:PassRole",
        Resource = aws_iam_role.lambda_exec.arn
      }
    ]
  })
}

# Attach IAM Policies to Lambda Role
resource "aws_iam_role_policy_attachment" "permissions_access_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_permissions.arn
}

# Attach AWS Managed Policy for Full Lambda Access
resource "aws_iam_role_policy_attachment" "lambda_full_access" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.lambda_source_dir
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  depends_on = [
    aws_iam_role_policy_attachment.permissions_access_attachment,
    aws_iam_role_policy_attachment.lambda_assume_role_attachment,
    aws_iam_role_policy_attachment.lambda_full_access
  ]

  function_name    = var.function_name
  handler          = var.handler
  runtime          = var.runtime
  role             = aws_iam_role.lambda_exec.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  layers = [
    "arn:aws:lambda:eu-central-1:555491921091:layer:psycopg2-layer:1",
    "arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-p311-requests:15"
  ]
}
