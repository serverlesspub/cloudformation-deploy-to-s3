DEPLOYMENT_BUCKET_NAME := desole-packaging
DEPLOYMENT_KEY := $(shell echo frontend-deploy-$$RANDOM.zip)
STACK_NAME := frontend-deploy-layer

clean: 
	rm -rf build

build/python: src/deployer.py
	mkdir -p build/python
	cp -R src/ build/python

build/layer.zip: build/python
	cd build/ && zip -r layer.zip python

build/function.zip: lambda
	cd lambda/ && zip -r ../build/function.zip *

# cloudformation has no support for packaging layers yet, so need to do this manually

build/output.yml: build/layer.zip cloudformation/template.yml build/function.zip
	aws s3 cp build/layer.zip s3://$(DEPLOYMENT_BUCKET_NAME)/$(DEPLOYMENT_KEY)/layer.zip
	aws s3 cp build/function.zip s3://$(DEPLOYMENT_BUCKET_NAME)/$(DEPLOYMENT_KEY)/function.zip
	sed "s:DEPLOYMENT_BUCKET_NAME:$(DEPLOYMENT_BUCKET_NAME):;s:DEPLOYMENT_KEY:$(DEPLOYMENT_KEY):" cloudformation/template.yml > build/output.yml

deploy: build/output.yml
	aws cloudformation deploy --template-file build/output.yml --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text