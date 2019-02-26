DEPLOYMENT_BUCKET_NAME ?= desole-packaging
DEPLOYMENT_KEY := $(shell echo s3-deployment-$$RANDOM.zip)
STACK_NAME ?= s3-deployment

clean: 
	rm -rf build

build/python: 
	mkdir -p build/python

build/python/deployer.py: src/deployer.py build/python
	cp $< $@

build/python/requests: build/python
	pip install requests --target build/python

build/layer.zip: build/python/deployer.py build/python/requests
	cd build/ && zip -r layer.zip python

deploy: cloudformation/template.yml build/layer.zip
	aws s3 cp build/layer.zip s3://$(DEPLOYMENT_BUCKET_NAME)/$(DEPLOYMENT_KEY)
	aws cloudformation deploy --template-file cloudformation/template.yml --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM --parameter-overrides DeploymentBucketName=$(DEPLOYMENT_BUCKET_NAME) DeploymentKey=$(DEPLOYMENT_KEY) LayerName=$(STACK_NAME)
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text
