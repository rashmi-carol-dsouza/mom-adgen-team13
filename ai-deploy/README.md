# Event Advert API Deployment

This project deploys an AWS Lambda function that generates event advertisements with background music. The function uses external libraries for text-to-speech conversion and audio processing, then returns (or saves) the generated MP3 file. The deployment is managed via Terraform for infrastructure (S3 bucket, IAM roles/policies, Lambda, API Gateway) and a Makefile to package and update the Lambda code.

## Directory Structure

```
.
├── lambda_function.py    # Python source code for the Lambda function
├── background.mp3        # Add background music file used for mixing audio
├── Makefile              # Script to package and deploy the Lambda function
└── main.tf               # Terraform configuration for all AWS resources
```

## Project Overview

- **Lambda Function:**  
  The function (named `event-advert-api`) uses libraries such as `pydub` for audio processing, along with custom modules (e.g., `lmnt.api` and `langchain_*` libraries) to generate a spoken advertisement. It fetches background music from S3, synthesizes speech, and overlays the two audio streams.

- **S3 Bucket:**  
  A bucket (named `event-advert-mp3-storage`) is created to store the background music file and (if needed) other audio assets.

- **IAM Roles and Policies:**  
  Terraform provisions a Lambda execution role with the necessary permissions to write logs, access S3, and interact with AWS Lambda.

- **API Gateway:**  
  An API Gateway REST API is configured with a resource path (`/generate-advert`) and a POST method that invokes the Lambda function using AWS_PROXY integration.

## Prerequisites

- **AWS Account:**  
  Ensure you have an active AWS account and credentials configured (using the AWS CLI or environment variables).

- **Terraform:**  
  Install Terraform from the [Terraform Downloads](https://www.terraform.io/downloads.html) page.

- **AWS CLI:**  
  Installed and configured for your target region (in this case, `eu-central-1`).

- **Dependencies:**  
  The Lambda function requires Python dependencies (e.g., `pydub`, `boto3`, etc.). These must be packaged along with your code or provided as a Lambda layer.

## Configuring Environment Variables in AWS

Important:
For security reasons, sensitive keys such as your LMNT and Mistral API keys are stored directly as AWS Lambda environment variables—set via the AWS Console or using secure mechanisms (like AWS Secrets Manager or Systems Manager Parameter Store)—instead of being defined in Terraform.

Your Lambda function expects the following environment variables to be set:

S3_BUCKET_NAME: Name of the S3 bucket (e.g., event-advert-mp3-storage).
LMNT_API_KEY: Your API key for the LMNT text-to-speech service.
MISTRAL_API_KEY: Your API key for the Mistral chat model service.

To update these values via the AWS CLI, for example, you might run:

```bash
aws lambda update-function-configuration \
  --function-name event-advert-api \
  --environment "Variables={S3_BUCKET_NAME=event-advert-mp3-storage,LMNT_API_KEY=your-lmnt-api-key,MISTRAL_API_KEY=your-mistral-api-key}" \
  --region eu-central-1
  ```
Ensure these environment variables are properly configured so that your Lambda function can retrieve them (e.g., via the helper function get_lambda_env_variable in your code).

## Setup and Deployment

### 1. Package the Lambda Function

The provided Makefile packages your Lambda code and background music into a ZIP file. Open your terminal and run:

```bash
make deploy
```

The Makefile will:
- Package `lambda_function.py` and `background.mp3` into `lambda_function.zip`
- Check if the Lambda function already exists (by name)
  - If it exists, update the code via the AWS CLI
  - Otherwise, initialize and apply your Terraform configuration to create all resources

### 2. Deploy Infrastructure with Terraform

If your Lambda function doesn’t exist yet or you need to recreate resources, change into the `terraform` directory and run:

```bash
cd terraform
terraform init
terraform plan
terraform apply --auto-approve
```

This creates the following AWS resources:
- **S3 Bucket:** `event-advert-mp3-storage`
- **IAM Role & Policy:** For Lambda execution with logging and S3 access
- **Lambda Function:** `event-advert-api` (runtime Python 3.11)
- **API Gateway REST API:** Named `EventAdvertAPI` with a resource at `/generate-advert`
- **Lambda Permissions:** Allowing API Gateway to invoke the Lambda function

### 3. Testing the API

After deployment, retrieve the API endpoint URL from Terraform’s output or by looking in the AWS API Gateway console. The endpoint URL typically looks like:

```
https://<rest_api_id>.execute-api.eu-central-1.amazonaws.com/prod/generate-advert
```

You can test the API using a tool like `curl`:

```bash
curl -X POST https://<rest_api_id>.execute-api.eu-central-1.amazonaws.com/prod/generate-advert \
     -H "Content-Type: application/json" \
     -d '{
           "event": {
             "artist_name": "The Sample Band",
             "event_type": "concert",
             "venue_name": "Sample Arena",
             "city": "Berlin",
             "country": "Germany",
             "event_start_date": "May 10",
             "event_start_time": "8 PM",
             "genres": ["rock", "pop"]
           }
         }'
```

The response should include a reference to the generated MP3 file (or return the file content, depending on your function’s implementation).

## Configuration Details

- **Lambda Environment Variables:**  
  The Lambda function expects certain environment variables (e.g., `S3_BUCKET_NAME`, `MISTRAL_API_KEY`, `LMNT_API_KEY`).  
  Update these via the AWS Console or extend the Terraform configuration if needed.

- **Terraform Variables:**  
  The `main.tf` file hardcodes the region to `eu-central-1` and bucket names. Adjust these as needed for your environment.

- **API Gateway Resource:**  
  The API Gateway resource is set up for the `/generate-advert` path and uses POST as the HTTP method.

## Debugging and Troubleshooting
### Common Issues
Missing Authentication Token:
Ensure you are calling the full API endpoint URL (including /generate-advert). A common mistake is invoking the base URL without the correct resource path.

Lambda Execution Errors:
Check the CloudWatch Logs for /aws/lambda/event-advert-api to review runtime errors or missing dependencies.

Debugging Lambda Layer Package Errors
If you encounter issues where the Lambda layer package is missing or not updating correctly, try the following commands:

```bash
# Delete all existing versions of the layer "event-advert-layer"
for version in $(aws lambda list-layer-versions --layer-name "event-advert-layer" --region eu-central-1 --query 'LayerVersions[*].Version' --output text); do 
    echo "Deleting Layer: event-advert-layer - Version: $version"
    aws lambda delete-layer-version --layer-name "event-advert-layer" --version-number "$version" --region eu-central-1
done

# List all layers to verify deletion
aws lambda list-layers --region eu-central-1

# Update the Lambda function configuration to use the correct layer version
aws lambda update-function-configuration \
    --function-name event-advert-api \
    --layers arn:aws:lambda:eu-central-1:[your layer id]:layer:event-advert-layer:[the layer number] \
    --region eu-central-1

# Invoke the Lambda function to test the new configuration and check the output
aws lambda invoke --function-name event-advert-api response.json --region eu-central-1
cat response.json
```

These commands help ensure that old or problematic layer versions are removed and that your Lambda function uses the correct, updated layer.

## Updating the Deployment

1. **Make Code or Config Changes:**  
   Edit `lambda_function.py` or your Terraform files as needed.

2. **Repackage and Redeploy:**  
   Run `make deploy` again to package your updated code and apply changes.

3. **Re-deploy API Gateway if Needed:**  
   Changes to API Gateway configuration may require a new deployment to be pushed.

## Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/index.html)

---

This README provides a comprehensive guide to deploying and maintaining your Event Advert API. Adjust configurations and environment variables as needed for your specific deployment scenario.