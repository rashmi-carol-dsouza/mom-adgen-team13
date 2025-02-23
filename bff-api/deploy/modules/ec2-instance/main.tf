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
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.this.id]
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y git python3
              cd /home/ec2-user
              git clone ${var.flask_app_repo_url} flask-app
              cd flask-app
              python3 -m pip install --upgrade pip
              if [ -f requirements.txt ]; then
                  python3 -m pip install -r requirements.txt
              else
                  python3 -m pip install Flask
              fi
              nohup python3 app.py &
              EOF

  tags = {
    Name = var.instance_name
  }
}
