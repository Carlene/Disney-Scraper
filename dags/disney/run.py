####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries ###########################################
from scraper import scrape_every_page
from organize_job_details import map_job_details_with_qualifications
from aws_info.upload_to_aws import upload_to_s3
######################## Use Case ##############################################
"""
Run this script to upload a CSV of Disney Data Engineering jobs to the specified S3 bucket
"""
################################################################################

# TODO: make job dictionary keys into tuples with job posting date and job id
# TODO: aggressively filter out postings without Data or Engineer
# TODO: find file using absolute paths

def create_csv(d):
    """ Creates a CSV from a dictionary!"""
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv("disney.csv")

def main():
    """Run all necessary functions. Return: None
    Goes through all pages in main Disney job search
    Scrapes the job links from each page
    And opens every link to pull job data to put into a CSV, then upload that data to S3
    Return: None
     """
    search_page_job_list = scrape_every_page()  
    all_job_details_by_id = map_job_details_with_qualifications(search_page_job_list)
    create_csv(all_job_details_by_id)
    upload_to_s3("disney.csv")

if __name__ == "__main__":
    main()