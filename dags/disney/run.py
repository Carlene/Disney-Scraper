####################### Standard Libraries #####################################
import pandas as pd
from datetime import datetime as dt
####################### My Libraries ###########################################
from scraper import scrape_every_page
from organize_job_details import map_job_details_with_qualifications
from aws_info.upload_to_aws import upload_to_s3
######################## Use Case ##############################################
"""
Run this script to upload a CSV of Disney Data Engineering jobs to the specified S3 bucket
"""
################################################################################

# TODO: scraper is pulling all data off pages then omitting data that isn't the correct date. 
# should check for date first and not pull data if it's the wrong date
# TODO: find file using absolute paths

def create_csv(d, date_pulled):
    """ Creates a CSV from a dictionary, with naming convention "datepulled_disney.csv" """
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv(f"{date_pulled}_disney.csv")

def main(start_date=""):
    """Run all necessary functions. Return: None
    Goes through all pages in main Disney job search
    Scrapes the job links from each page
    Opens every link to pull job data to put into a CSV
    Then uploads that data to the S3
    Return: None
     """
    today = dt.today().date()
    if start_date != "":
        start_date = dt.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = today
    search_page_job_list = scrape_every_page()  
    all_job_details_by_id = map_job_details_with_qualifications(search_page_job_list, start_date=start_date)
    create_csv(all_job_details_by_id, start_date)
    # upload_to_s3("disney.csv")

if __name__ == "__main__":
    main()