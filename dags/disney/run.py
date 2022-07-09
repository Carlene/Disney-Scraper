####################### Standard Libraries #####################################
import pandas as pd
from datetime import datetime as dt, timedelta
import numpy as np
import schedule
import time
####################### My Libraries ###########################################
from scraper import scrape_every_page
from organize_job_details import map_job_details_with_qualifications
from aws_info.upload_to_aws import upload_to_s3, execute_query, rsd_client
from clean_disney_data import create_csv, split_up_dataframe
from aws_info.queries import *
######################## Use Case ##############################################
"""
Run this script to upload a CSV of Disney Data Engineering jobs to the specified S3 bucket
"""
################################################################################

# TODO: scraper is pulling all data off pages then omitting data that isn't the correct date. 
# should check for date first and not pull data if it's the wrong date, to make backfilling faster
# TODO: find file using absolute paths

def create_s3_file_path(file_string):
    s3_file_path = "_".join(file_string.split("_")[:2]) # file name for s3 will be first two words in file path
    s3_file_path += ".csv"
    return s3_file_path

def main(start_date:str = "", pages:int = ""):
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
    print(start_date)
    
    search_page_job_list = scrape_every_page(pages=pages) # scrape meta data from main job search page
    all_job_details_by_id = map_job_details_with_qualifications(search_page_job_list, start_date=start_date) # map main page data with inner page data
    raw_disney_df, file_string = create_csv(all_job_details_by_id, date_pulled=start_date) # raw pull before keyword cleaning
    s3_file_path = create_s3_file_path(file_string) 
    upload_to_s3(file_string, s3_file_path) 
 
    dfs = split_up_dataframe(raw_disney_df, start_date) # create different dataframes for dimension, location, education, and qualifications data cause redshift doesn't letcha unnest lists 
    table_names = ["dimension_table", "locations_table", "education_table", "qualifications_table"]
    for i in range(len(dfs)):  # create a csv file for each df to eventually upload to s3
        file_string = create_csv(dfs[i], file_string = f"{table_names[i]}_", date_pulled=start_date)[1] 
        s3_file_path = create_s3_file_path(file_string)
        upload_to_s3(file_string, s3_file_path) 
    # now upload data to redshift
    execute_query(rsd_client, copy_disney_tables_query) # update disney tables
    execute_query(rsd_client, all_data_query) # update combined tables

# def job():
#     print("Running scraper now!")
#     # change for start date and amount of pages wanted (defaults to yesterday and for all pages)
#     main(pages=1)
    
# schedule.every().day.at("22:30").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    # change for start date and amount of pages wanted (defaults to yesterday and for all pages)
    main(pages=1)