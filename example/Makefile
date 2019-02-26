BUCKET_NAME ?= desole-packaging
STACK_NAME ?= s3-deployment-example
REGION := us-east-1

clean: 
	rm output-*.yml

output-%.yml: template-%.yml web-site/*
	aws cloudformation package --template-file $< --output-template-file $@ --s3-bucket=$(BUCKET_NAME) --region $(REGION)

deploy-%: output-%.yml
	aws cloudformation deploy --template-file $< --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --region $(REGION)
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text --region $(REGION)
