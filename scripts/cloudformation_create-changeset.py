from __future__ import print_function
import argparse
import sys
import boto3
from botocore.exceptions import ClientError

def create_changeset(template, stackname, changesetname):
    """
    Creates a changeset on the specified stack using the specified template
    """
    try:
        client = boto3.client('cloudformation')
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False

    try:
        response = client.create_change_set(
            StackName=stackname,
            TemplateURL=template,
            ChangeSetName=changesetname
        )
        return response
    except ClientError as err:
        print("Failed to create change set.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access " + template + ".\n" + str(err))
        return False

def main():
    parser = argparse.ArgumentParser(description='Creates a Cloudformation changeset to a stack with an existing template in s3')
    parser.add_argument('--template', help='S3 path where to find the template')
    parser.add_argument('--stackname', help='Cloudformation stack to create the changeset on')
    parser.add_argument('--changesetname', help='Cloudformation changeset name to be created by this call')
    args = parser.parse_args()

    result = create_changeset(args.template, args.stackname, args.changesetname)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
