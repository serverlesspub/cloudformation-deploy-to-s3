import os
import boto3
import mimetypes
import json
import requests
import subprocess
import tempfile

s3 = boto3.resource('s3')

def resource_handler(event, context):
  print(event)
  try:
    target_bucket = event['ResourceProperties']['TargetBucket']
    lambda_src = os.getcwd()
    acl = event['ResourceProperties']['Acl']
    cacheControl = 'max-age=' + \
        event['ResourceProperties']['CacheControlMaxAge']
    print(event['RequestType'])
    if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
      
      if 'Substitutions' in event['ResourceProperties'].keys():
        lambda_src = apply_substitutions(event['ResourceProperties']['Substitutions'])

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
        upload_file(source_file_path, target_bucket,
                    destination_s3_key, s3, acl, cacheControl, contentType)


def upload_file(source, bucket, key, s3lib, acl, cacheControl, contentType):
    print('uploading from {} {} {}'.format(source, bucket, key))
    s3lib.Object(bucket, key).put(ACL=acl, Body=open(source, 'rb'),
                                  CacheControl=cacheControl, ContentType=contentType)


def send_result(event):
  response_body = json.dumps({
    'Status': 'SUCCESS',
    'PhysicalResourceId': get_physical_resource_id(event),
    'StackId': event['StackId'],
    'RequestId': event['RequestId'],
    'LogicalResourceId': event['LogicalResourceId']
  })
  print(response_body)
  requests.put(event['ResponseURL'], data=response_body)


def send_error(event, error):
  response_body = json.dumps({
    'Status': 'FAILED',
    'Reason': str(error),
    'PhysicalResourceId': get_physical_resource_id(event),
    'StackId': event['StackId'],
    'RequestId': event['RequestId'],
    'LogicalResourceId': event['LogicalResourceId']
  })
  print(response_body)
  requests.put(event['ResponseURL'], data=response_body)

def get_physical_resource_id(event):
  if 'PhysicalResourceId' in event.keys():
    return event['PhysicalResourceId']
  else:
    return event['RequestId']

def apply_substitutions(substitutions):
  if not 'Values' in substitutions.keys():
    raise ValueError('Substitutions must contain Values')

  if not isinstance(substitutions['Values'], dict):
    raise ValueError('Substitutions.Values must be an Object')

  if len(substitutions['Values']) < 1:
    raise ValueError('Substitutions.Values must not be empty')

  if not 'FilePattern' in substitutions.keys():
    raise ValueError('Substitutions must contain FilePattern')

  if not isinstance(substitutions['FilePattern'], str):
    raise ValueError('Substitutions.FilePattern must be a String')

  if len(substitutions['FilePattern']) < 1:
    raise ValueError('Substitutions.FilePattern must not be empty')

  values = substitutions['Values']
  file_pattern = substitutions['FilePattern']

  temp_dir = tempfile.mkdtemp()
  sub_dir = os.path.join(temp_dir, 'src')
  subprocess.run(['cp', '-r', os.getcwd(), sub_dir])

  full_path = os.path.join(sub_dir, 'index.html')
  sed_script = ';'.join(list(map(lambda key: str.format('s/{}/{}/g', sed_escape(key), sed_escape(values[key])), values.keys())))
  print('sed script', sed_script)
  subprocess.run(['sed', sed_script, '-i', full_path], cwd=tempfile.gettempdir(), check=True)

  return sub_dir

def sed_escape(text):
 return text.replace('/', '\\/')
