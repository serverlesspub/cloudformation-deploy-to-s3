import os
import boto3
import mimetypes
s3 = boto3.resource('s3')

def handler(event, context):
  target_bucket = os.environ['TARGET_BUCKET']
  lambda_src = os.getcwd()
  acl = 'private'
  cacheControl = 'max-age=600'
  
  upload(lambda_src, target_bucket, acl, cacheControl)
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