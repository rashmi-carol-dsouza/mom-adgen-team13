module "lambda" {
  source            = "./modules/lambda"
  function_name     = "generated_ads_lambda"
  handler           = "lambda_function.lambda_handler"
  runtime           = "python3.11"
  lambda_source_dir = "../lambda"
  region            = var.region
  tags              = var.tags
}

module "api_gateway" {
  source                = "./modules/api_gateway"
  lambda_function_arn   = module.lambda.lambda_arn
  lambda_function_name  = "generated_ads_lambda"
  stage_name            = var.stage_name
  region                = var.region
  tags                  = var.tags
}
