import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv('.env')

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
# BUCKET_NAME = os.environ.get('BUCKET_NAME', 'webcorebucket')


def upload_to_aws(local_file, bucket, s3_file):
    print(ACCESS_KEY, SECRET_KEY)
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    print(ACCESS_KEY, SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return s3_file, {"msg": "Upload Successful"}
    except FileNotFoundError:
        print("The file was not found")
        return False, {"msg": "File was not found"}
    except NoCredentialsError:
        print("Credentials not available")
        return False, {"msg": "Credentials not valid"}


def download_from_aws(bucket, s3_file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.download_file(bucket, s3_file, file_name)
        print("download Successful")
        return True, {"msg": "File Downloaded. Please check"}
    except FileNotFoundError:
        print("The file was not found")
        return False, {"msg": "File was not found"}
    except NoCredentialsError:
        print("Credentials not available")
        return False, {"msg": "Credentials not available"}

def download_file_obj(bucket, s3_file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        file = s3.get_object(Bucket=bucket,Key=s3_file)
        print("download Successful")
        return file
    # except FileNotFoundError:
    #     print("The file was not found")
    #     return file
    except Exception as e:
        print("Credentials not available",e)
        return None



# file_name = upload_to_aws('/content/sample_data/mnist_test.csv', 'webcorebucket', 'test/mnist_test.csv')
