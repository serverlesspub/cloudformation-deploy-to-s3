STACK_NAME ?= s3-deployment-example

clean: 
	rm output.yml

output.yml: template.yml web-site/*
	aws cloudformation package --template-file $< --output-template-file $@ --s3-bucket=$(DEPLOYMENT_BUCKET_NAME)

deploy: output.yml
	aws cloudformation deploy --template-file $< --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text
