####################### My Libraries ###########################################
from aws_info.aws_secrets import *

# creating queries in my S3

# create_table_query = """
#     CREATE SCHEMA disney;
#     DROP TABLE IF EXISTS disney.data_engineering_postings;
#     CREATE TABLE disney.data_engineering_postings(
#         id int,
#         path varchar,
#         title varchar,
#         brand varchar,
#         locations varchar,
#         posting_date varchar,
#         responsibilities varchar,
#         basic_qualifications varchar,
#         preferred_qualifications varchar,
#         education varchar,
#         preferred_education varchar,
#         key_qualifications varchar,
#         nice_to_haves varchar
#     );
# """

# copy_table_query = f"""
#     COPY disney.data_engineering_postings FROM '{s3_file_link}'
#     IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
#     DELIMITER ','
#     IGNOREHEADER 1; """

# creation queries in Will's S3

all_data_query = """
    DROP TABLE IF EXISTS project.staged_disney_data_jobs;

    CREATE TABLE project.staged_disney_data_jobs(
        id VARCHAR(1000),
        title VARCHAR(1000),
        locations VARCHAR(1000),
        posting_date VARCHAR(1000),
        education VARCHAR(1000),
        qualifications VARCHAR(1000)
        );

    DROP TABLE IF EXISTS project.disney_data_jobs;

    CREATE TABLE project.disney_data_jobs AS
    SELECT *
    FROM project.staged_disney_data_jobs
    WHERE title ILIKE '%data%';

    DROP TABLE IF EXISTS project.staged_disney_data_jobs;
"""

tables = [
    "dimension_table_disney.csv", 
    "locations_table_disney.csv", 
    "qualifications_table_disney.csv", 
    "education_table_disney.csv"]

copy_table_query = f"""
    COPY insert_table_here
    FROM {s3_file_link}
    REGION 'us-west-1'
    IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
    DELIMITER ','
    IGNOREHEADER 1
    emptyasnull
    blanksasnull
    removequotes;
"""