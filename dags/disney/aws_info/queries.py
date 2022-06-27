####################### My Libraries ###########################################
from aws_info.aws_secrets import *

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
    COPY disney.data_engineering_postings FROM '{s3_file_path}'
    IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
    DELIMITER ','
    IGNOREHEADER 1; """
