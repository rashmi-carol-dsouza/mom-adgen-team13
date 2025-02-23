resource "aws_iam_role" "deploy_role" {
  name = var.deploy_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          AWS = var.allowed_principals
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "deploy_policy" {
  name        = "${var.deploy_role_name}_policy"
  description = "Policy to allow deployment of Lambda and S3 resources"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "lambda:*",
          "s3:*",
          "iam:PassRole",
           "ssm:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "deploy_policy_attach" {
  role       = aws_iam_role.deploy_role.name
  policy_arn = aws_iam_policy.deploy_policy.arn
}
