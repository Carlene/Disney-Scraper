####################### Standard Libraries #####################################
# import importlib  
# disney_scraper = importlib.import_module("Disney-Scraper")
import pandas as pd
import boto3
from aws_info.aws_secrets import s3_access_key_id, s3_secret_access_key, s3_bucket
################################# My Libraries #################################
from scraper import scrape_every_page
import organize_job_details as organize
################################################################################

# TODO: make job dictionary keys into tuples with job posting date and job id
# TODO: aggressively filter out postings without Data or Engineer
# TODO: find file using absolute paths

def upload_to_s3(csv):
    """Takes a csv file and uploads it to my bucket in S3. Prints error if there is one. Return: None"""
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


def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv("disney.csv")

def main():
    """Run all necessary functions. Return: None """
    pages = 1 # comment out when script runs properly 
    search_page_job_list = scrape_every_page(pages) # comment out pages when script runs properly 
    all_job_details_by_id = organize.map_job_details_with_qualifications(search_page_job_list)
    create_csv(all_job_details_by_id)
    upload_to_s3("disney.csv")

if __name__ == "__main__":
    main()