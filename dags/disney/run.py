####################### Standard Libraries #####################################
import pandas as pd
from datetime import datetime as dt, timedelta
import numpy as np
####################### My Libraries ###########################################
from dags.disney.scraper import scrape_every_page
from dags.disney.organize_job_details import map_job_details_with_qualifications
from dags.disney.aws_info.upload_to_aws import upload_to_s3
from dags.disney.filter_job_results import find_keywords
######################## Use Case ##############################################
"""
Run this script to upload a CSV of Disney Data Engineering jobs to the specified S3 bucket
"""
################################################################################

# TODO: oh yeah, jobs can get DELETED. backfilling isn't really a thing, only need to scrape all jobs currently there
# TODO: scraper is pulling all data off pages then omitting data that isn't the correct date. 
# should check for date first and not pull data if it's the wrong date, to make backfilling faster
# TODO: find file using absolute paths


def create_csv(data, date_pulled=""):
    """ 
    When given a dictionary, creates a CSV file from the data (pretty unclean data from disney) named
    When given a dataframe, applies more filtering functions, and only returns necessary columns to create a CSV file for Redshift
    """
    if type(data) == dict: # just give us everything 
        disney_data = pd.DataFrame.from_dict(data, orient="index")
        disney_data.to_csv(f"raw_{date_pulled}_disney.csv")
    else: # try to only give keywords instead of literally all the strings
        try:
            disney_data = pd.read_csv(data)
        except Exception as e:
            print(f"This isn't a CSV file: {e}")
        disney_data = find_keywords(disney_data)
        disney_data.to_csv(f"{date_pulled}_disney.csv")
    print("All done!")
    return disney_data.head()


def main(start_date=""):
    """Run all necessary functions. Return: None
    Goes through all pages in main Disney job search
    Scrapes the job links from each page
    Opens every link to pull job data to put into a CSV
    Then uploads that data to the S3
    Return: None
     """
    yesterday = dt.today().date()-timedelta(days=1)
    if start_date != "": # scrape for job postings from given start date (to backfill)
        start_date = dt.strptime(start_date, '%Y-%m-%d').date()
    else: # scrape for yesterday's job postings
        start_date = yesterday
    search_page_job_list = scrape_every_page()  
    all_job_details_by_id = map_job_details_with_qualifications(search_page_job_list, start_date=start_date)
    create_csv(all_job_details_by_id, start_date) # raw pull
    print(create_csv("disney.csv")) # cleaned pull
    # upload_to_s3("disney.csv")

if __name__ == "__main__":
    # change for start date wanted
    main(start_date="")