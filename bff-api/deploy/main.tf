module "ec2_instance" {
  source              = "./modules/ec2-instance"
  instance_name       = var.instance_name
  instance_type       = var.instance_type
  ami_id              = var.ami_id
  vpc_id              = var.vpc_id
  subnet_id           = var.subnet_id
  allowed_cidr_blocks = var.allowed_cidr_blocks
  flask_app_repo_url  = var.flask_app_repo_url
}
