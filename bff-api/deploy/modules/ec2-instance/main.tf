resource "aws_iam_role" "cloudwatch_role" {
  name = "${var.instance_name}_cloudwatch_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name        = "${var.instance_name}_cloudwatch_policy"
  description = "Allows EC2 to write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cloudwatch_attachment" {
  role       = aws_iam_role.cloudwatch_role.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

resource "aws_iam_instance_profile" "cloudwatch_profile" {
  name = "${var.instance_name}_cloudwatch_profile"
  role = aws_iam_role.cloudwatch_role.name
}

resource "aws_cloudwatch_log_group" "flask_logs" {
  name = "/ec2/${var.instance_name}/flask"
  retention_in_days = 7
}

resource "aws_security_group" "this" {
  name        = "${var.instance_name}-sg"
  description = "Security group for the Flask app"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow HTTP traffic on port 5000"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  ingress {
    description = "Allow SSH traffic on port 22"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.this.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.cloudwatch_profile.name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y git python3 amazon-cloudwatch-agent
              cd /home/ec2-user
              python3 -m pip install poetry
              git clone ${var.flask_app_repo_url} mom-adgen-team13
              cd mom-adgen-team13/bff-api
              make setup

              # CloudWatch Agent Configuration
              cat > /opt/aws/amazon-cloudwatch-agent/etc/cloudwatch-config.json <<EOL
              {
                "logs": {
                  "logs_collected": {
                    "files": {
                      "collect_list": [
                        {
                          "file_path": "/home/ec2-user/mom-adgen-team13/bff-api/logs/app.log",
                          "log_group_name": "/ec2/${var.instance_name}/flask",
                          "log_stream_name": "{instance_id}"
                        }
                      ]
                    }
                  }
                }
              }
              EOL

              systemctl enable amazon-cloudwatch-agent
              systemctl start amazon-cloudwatch-agent

              make run
              EOF

  tags = {
    Name = var.instance_name
  }
}
