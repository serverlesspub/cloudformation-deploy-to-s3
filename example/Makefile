BUCKET_NAME := desole-packaging
STACK_NAME := s3-deployment-example-2

output.yml: template.yml src/*
	aws cloudformation package --template-file $< --output-template-file $@ --s3-bucket=$(BUCKET_NAME)

deploy: output.yml
	aws cloudformation deploy --template-file $< --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM
	@echo 'listing bucket'
	@aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text
	@aws s3 ls s3://$(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text) --recursive