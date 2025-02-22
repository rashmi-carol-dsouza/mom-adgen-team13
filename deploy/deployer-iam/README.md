# Deployer IAM

This collection of Terraform files allows the manual, cli based creation of AWS resources on a single AWS account by users of different accounts. Why? To keep the deployments simple for this hackathon.

## How to use this in your deployment

1. Install Terraform and AWS CLI
2. Configure AWS Credentials - Developers need AWS credentials (access key and secret) that have permission to assume the role created by Terraform. Typically, this will be their IAM user credentials.
3. Assume the role - To use the deployment role, developers should configure their AWS CLI (or their environment variables) to assume the role. This can be done by adding a profile to their AWS configuration file `(~/.aws/config)` like:

```
[profile deployment]
role_arn = arn:aws:iam::<LARRYS_ACCOUNT_ID>:role/deployment_role
source_profile = default
region = us-east-1
```

4. This will return temporary credentials (Access Key, Secret Key, and Session Token) which can be set as environment variables before running Terraform:

```sh
export AWS_ACCESS_KEY_ID=<temporary-access-key>
export AWS_SECRET_ACCESS_KEY=<temporary-secret-key>
export AWS_SESSION_TOKEN=<temporary-session-token>
```

5. Run `terraform plan` to see the plan and to deploy `terraform apply`
