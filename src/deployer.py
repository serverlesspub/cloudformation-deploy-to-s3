import os
import boto3
import mimetypes
import json
import requests

s3 = boto3.resource('s3')

def resource_handler(event, context):
  print(event)
  try:
    target_bucket = event['ResourceProperties']['TargetBucket']
    lambda_src = os.getcwd()
    acl = event['ResourceProperties']['Acl']
    cacheControl = 'max-age=' + event['ResourceProperties']['CacheControlMaxAge']
    print(event['RequestType'])
    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
      print('uploading')
      upload(lambda_src, target_bucket, acl, cacheControl)
    else:
      print('ignoring')
    
    send_result(event)
  except Exception as err:
    send_error(event, err)
  return event

def upload(lambda_src, target_bucket, acl, cacheControl):
  for folder, subs, files in os.walk(lambda_src):
    for filename in files:
        source_file_path = os.path.join(folder, filename)
        destination_s3_key = os.path.relpath(source_file_path, lambda_src)
        contentType, encoding = mimetypes.guess_type(source_file_path)
        upload_file(source_file_path, target_bucket, destination_s3_key, s3, acl, cacheControl, contentType)

def upload_file(source, bucket, key, s3lib, acl, cacheControl, contentType):
    print('uploading from {} {} {}'.format(source, bucket, key))
    s3lib.Object(bucket, key).put(ACL=acl,Body=open(source, 'rb'),CacheControl=cacheControl,ContentType=contentType)

def send_result(event):
  response_body = json.dumps({
    'Status': 'SUCCESS',
		'PhysicalResourceId': 'zeka123',
		'StackId': event['StackId'],
		'RequestId': event['RequestId'],
		'LogicalResourceId': event['LogicalResourceId']
  })
  print(response_body)
  requests.put(event['ResponseURL'], data = response_body)

def send_error(event, error):
  response_body = json.dumps({
    'Status': 'FAILED',
    'Reason': str(error),
		'PhysicalResourceId': event['PhysicalResourceId'] or event['RequestId'],
		'StackId': event['StackId'],
		'RequestId': event['RequestId'],
		'LogicalResourceId': event['LogicalResourceId']
  })
  print(response_body)
  requests.put(event['ResponseURL'], data = response_body)