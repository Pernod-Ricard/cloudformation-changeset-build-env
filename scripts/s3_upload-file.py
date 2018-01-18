from __future__ import print_function
import argparse
import sys
import boto3
from botocore.exceptions import ClientError

def upload_to_s3(bucket, file, key):
    """
    Uploads a file to a s3 bucket at the specified key
    """
    try:
        client = boto3.client('s3')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        response = client.put_object(
            Body=open(file, 'rb').read(),
            Bucket=bucket,
            Key=key
        )
        return response
    except ClientError as err:
        print("Failed to upload file.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access " + file + ".\n" + str(err))
        return False

def main():
    parser = argparse.ArgumentParser(description='Uploads a file to a S3 bucket at the specified key')
    parser.add_argument('--bucket', help='The S3 Bucket you want to upload to')
    parser.add_argument('--file', help='The file to upload to S3')
    parser.add_argument('--key', help='The key assigned to the uploaded key')
    args = parser.parse_args()

    result = upload_to_s3(args.bucket, args.file, args.key)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
