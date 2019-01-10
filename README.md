# CloudFormation Deploy to S3


Before the official announcement for this deployment, if you wanted to deploy your SPA app, along with your other serverless services, to try it out, in the `/example` directory, run:

`make deploy STACK_NAME=<name of cf stack> BUCKET_NAME=<s3 cloudformation deployment bucket>` 

For an explanation of how this works, check out the example [`template.yml`](example/template.yml)

**Note**: If you change your frontend folder from the current `web-site` into something else, be sure to replace it in its `template.yml` `SiteSource`, property `CodeUri`.
