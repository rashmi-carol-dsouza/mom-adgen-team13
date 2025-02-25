LAMBDA_NAME=event-advert-api
REGION=eu-central-1
ZIP_FILE=lambda_function.zip

deploy:
	@echo "Packaging Lambda..."
	zip -q $(ZIP_FILE) lambda_function.py background.mp3
	@echo "Deploying Lambda..."

	# Check if Lambda exists
	@if aws lambda get-function --function-name $(LAMBDA_NAME) --region $(REGION) > /dev/null 2>&1; then \
		echo "Updating Lambda..."; \
		aws lambda update-function-code --function-name $(LAMBDA_NAME) --zip-file fileb://$(ZIP_FILE) --region $(REGION); \
	else \
		echo "Creating Lambda..."; \
		terraform init && terraform apply --auto-approve; \
	fi

	@echo "Deployment complete!"
