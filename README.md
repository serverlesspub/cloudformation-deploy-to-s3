# CloudFormation Deploy to S3

Deploy and publish Frontend SPA apps, UI components, static websites and MicroFrontends to S3 and Serverless Application Repository using this Lambda Layer component.

For more information, see [How to use CloudFormation to deploy Frontend Apps to S3 and Serverless Application Repository](https://serverless.pub/deploy-frontend-to-s3-and-sar/).

## Deploying the example

There is a full example of a website to be deployed to S3 in the `example` directory, including applying substitutions to files.

To deploy it, in the `example` directory, run:

`make deploy STACK_NAME=<name of cf stack> DEPLOYMENT_BUCKET_NAME=<s3 cloudformation deployment bucket>`

## Usage instructions

The easiest place to deploy this is from the [Serverless App Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:375983427419:applications~deploy-to-s3)

```yml
  DeploymentLayer:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: arn:aws:serverlessrepo:us-east-1:375983427419:applications/deploy-to-s3
        SemanticVersion: 2.4.2

  SiteSource:
    Type: AWS::Serverless::Function
    Properties:
      Layers:
        - !GetAtt DeploymentLayer.Outputs.Arn
      CodeUri: web-site/
      AutoPublishAlias: live
      Runtime: python3.6
      Handler: deployer.resource_handler
      Timeout: 600
      Policies:
        - S3FullAccessPolicy:
            BucketName: !Ref TargetBucket
  DeploymentResource:
    Type: AWS::CloudFormation::CustomResource
    Properties:
      ServiceToken: !GetAtt SiteSource.Arn
      Version: !Ref "SiteSource.Version"
      TargetBucket: !Ref TargetBucket

      Substitutions:
        FilePattern: "*.html"
        Values:
          APP_NAME: 'Example Application'
          STACK_ID: !Ref AWS::StackId
      Acl: 'public-read'
      CacheControlMaxAge: 600
```

For full instructions and *code comments* please take a look at the example [template.yml](example/template.yml)

## Deployment from the source

For deploying your SPA app, along with your other serverless services, to try it out, in the `/example` directory, run:

`make deploy STACK_NAME=<name of cf stack> DEPLOYMENT_BUCKET_NAME=<s3 cloudformation deployment bucket>`
