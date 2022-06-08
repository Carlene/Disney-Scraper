####################### Standard Libraries #####################################
import sys
sys.dont_write_bytecode = True
import boto3
import os
####################### My Libraries ###########################################
from aws import s3_access_key_id, s3_secret_access_key, s3_bucket

# TODO: loop through files in directory, only grab necessary files, upload to S3
# create a client to access resources with


def find_disney_folders():
    return os.getcwd()


def s3_info():
    s3_client = boto3.client(
        "s3", 
        aws_access_key_id = s3_access_key_id,
        aws_secret_access_key = s3_secret_access_key
    )
    object_name = "disney-scraper"

    return s3_client, object_name



# def find_disney_folders():

# # upload the applications to the bucket created earlier
#     s3_client, object_name = s3_info()
#     try:
#         s3_client.upload_file(file, s3_bucket, object_name)
#         print('File successfully loaded')
#     except:
#         print('Client error: file could not be uploaded to S3')