from __future__ import print_function
import argparse
import sys
import boto3
from botocore.exceptions import ClientError

def execute_change_set(stackname, changesetname):
    """
    Executes a change set to the AWS Cloudformation stack
    """
    client = boto3.client('cloudformation')
    if not client:
        return False

    try:
        result = client.execute_change_set(
            ChangeSetName=changesetname,
            StackName=stackname
        )
        return result
    except ClientError as err:
        print("Failed to create client.\n" + str(err))
        return False

def wait_change_set(stackname, changesetname):
    """
    Creates a change set to the AWS Cloudformation stack
    """
    try :
        client = boto3.client('cloudformation')
        if not client:
             return False
        waiter = client.get_waiter('change_set_create_complete')
        if not waiter:
             return False

        waiter.wait(
            StackName=stackname,
            ChangeSetName=changesetname
        )
        return True
    except ClientError as err:
        print("Failed to create client.\n" + str(err))
        return False

def main():
    parser = argparse.ArgumentParser(description='Executes a Cloudformation change on a stack after waiting for its creation.')
    parser.add_argument('--stackname', help='The Cloudformation stack name to execute the changeset on')
    parser.add_argument('--changesetname', help='The Cloudformation changeset to execute after its creation')
    args = parser.parse_args()

    result = wait_change_set(args.stackname, args.changesetname)
    if not result:
        sys.exit(1)
    result = execute_change_set(args.stackname, args.changesetname)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
