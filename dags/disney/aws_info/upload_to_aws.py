####################### Standard Libraries #####################################
import boto3
import botocore.session as bs
####################### My Libraries ###########################################
from dags.disney.aws_info.aws_secrets import *
############################# Use Case #########################################
"""
This script holds functions that will upload the CSV file created by the Disney scraper to the specified S3 bucket.
Then it uploads the data from the S3 bucket into a Redshift table
"""
################################################################################

def upload_to_s3(csv):
    """Takes a csv file and uploads to the specified S3 bucket. Prints error message if there is one. Return: None"""
    s3_client = boto3.client(
        "s3", 
        aws_access_key_id = s3_access_key_id,
        aws_secret_access_key = s3_secret_access_key
    )

    file = csv
    object_name = "dags/disney/disney.csv"

    # now upload to bucket 
    try:
        s3_client.upload_file(file, s3_bucket, object_name)
        print("File successfully uploaded")
    except Exception as e:
        print(f"File could not be uploaded to S3 because: {e}")


# creating queries
create_table_query = """
    CREATE SCHEMA disney;
    DROP TABLE IF EXISTS disney.data_engineering_postings;
    CREATE TABLE disney.data_engineering_postings(
        id int,
        path varchar,
        title varchar,
        brand varchar,
        locations varchar,
        posting_date varchar,
        responsibilities varchar,
        basic_qualifications varchar,
        preferred_qualifications varchar,
        education varchar,
        preferred_education varchar,
        key_qualifications varchar,
        nice_to_haves varchar
    );
"""

copy_table_query = f"""
    COPY disney.data_engineering_postings FROM "s3://disney-scraper/dags/disney/"
    IAM_ROLE "arn:aws:iam::{IAM_id}:role/AWSServiceRoleForRedshift"
    DELIMITER ","
    IGNOREHEADER 1; """


# create redshift data client
session = bs.get_session()
rsd_session = boto3.Session(botocore_session=session, region_name=aws_region)
# UPDATE the session client below with the proper access keys
rsd_client = rsd_session.client(
    'redshift-data'
    , aws_access_key_id = s3_access_key_id
    , aws_secret_access_key = s3_secret_access_key)


# define query execution and result retrieval methods using client
def execute_query(client, sql_query, query_note=None):
    # use client to execute statement
    desc, query_id = None, None
    try:
        # show note of what query is running
        print(f"Currently running: {query_note} query")

        # UPDATE this object to include the parameters needed to retrieve data
        response = client.execute_statement(
            ClusterIdentifier = cluster_id,
            Database = redshift_db,
            DbUser = redshift_user,
            Sql = sql_query
        )

        # check status of query with the describe statement method
        query_id = response['Id']
    except Exception as e:
        print(f"Could not execute statement and retrieve results because: {e}")
    return query_id

# uncomment when you want to make changes to redshift
# execute_query(rsd_client, create_table_query)
# execute_query(rsd_client, copy_table_query)