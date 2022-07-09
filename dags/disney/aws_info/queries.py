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

copy_disney_tables_query = f"""
DELETE FROM project.disney_dimensions
WHERE TRUE;

COPY project.disney_dimensions 
FROM 's3://project-team10/disney/dimension_table.csv'
REGION 'us-west-1'
IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
DELIMITER ','
IGNOREHEADER 1
emptyasnull
blanksasnull
removequotes;

----------------------------------------------------------------------------------
DELETE FROM project.disney_locations
WHERE TRUE;

COPY project.disney_locations 
FROM 's3://project-team10/disney/locations_table.csv'
REGION 'us-west-1'
IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
DELIMITER ','
IGNOREHEADER 1
emptyasnull
blanksasnull
removequotes;

----------------------------------------------------------------------------------
DELETE FROM project.disney_education
WHERE TRUE;

COPY project.disney_education 
FROM 's3://project-team10/disney/education_table.csv'
REGION 'us-west-1'
IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
DELIMITER ','
IGNOREHEADER 1
emptyasnull
blanksasnull
removequotes;

----------------------------------------------------------------------------------
DELETE FROM project.disney_qualifications
WHERE TRUE;

COPY project.disney_qualifications 
FROM 's3://project-team10/disney/qualifications_table.csv'
REGION 'us-west-1'
IAM_ROLE 'arn:aws:iam::{IAM_id}:role/{redshift_role}'
DELIMITER ','
IGNOREHEADER 1
emptyasnull
blanksasnull
removequotes;
"""


all_data_query = """
-- locations table
DELETE FROM project.all_job_locations
WHERE company = 'disney';

insert into project.all_job_locations(job_id, location, company)
  select 
  	dim_id as job_id,
  	locations as location,
    'disney' as company
  from project.disney_locations

-- qualifications table
DELETE FROM project.all_job_qualifications
WHERE company = 'disney';

insert into project.all_job_qualifications(job_id, qualification, company)
  select 
  	dim_id as job_id,
  	qualification,
    'disney' as company
  from project.disney_qualifications
--  
-- education table
DELETE FROM project.all_job_education
WHERE company = 'disney';

insert into project.all_job_education(job_id, education, company)
  select 
  	dim_id as job_id,
  	education_type as education,
    'disney' as company
  from project.disney_education
  
-- dimension table
DELETE FROM project.all_job_dimensions
WHERE company = 'disney';

insert into project.all_job_dimensions(job_id, title, posting_date, company)
  select 
  	dim_id as job_id,
  	title,
    posting_date,
    'disney' as company
  from project.disney_dimensions

"""