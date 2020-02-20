clean: 
	rm -rf build

build/python: 
	mkdir -p build/python

build/python/deployer.py: src/deployer.py build/python
	cp $< $@

build/python/requests: build/python
	pip install requests --target build/python

output.yml: cloudformation/template.yml build/python/requests build/python/deployer.py
	aws cloudformation package --template-file $< --output-template-file $@ --s3-bucket $(DEPLOYMENT_BUCKET_NAME)

deploy: output.yml
	aws cloudformation deploy --template-file $< --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM
	aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query Stacks[].Outputs[].OutputValue --output text

publish: output.yml
	sam publish -t output.yml
