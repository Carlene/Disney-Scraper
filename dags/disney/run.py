####################### Standard Libraries #####################################
import pandas as pd
from datetime import datetime as dt, timedelta
####################### My Libraries ###########################################
from dags.disney.scraper import scrape_every_page
from dags.disney.organize_job_details import map_job_details_with_qualifications
from dags.disney.aws_info.upload_to_aws import upload_to_s3
######################## Use Case ##############################################
"""
Run this script to upload a CSV of Disney Data Engineering jobs to the specified S3 bucket
"""
################################################################################

# TODO: scraper is pulling all data off pages then omitting data that isn't the correct date. 
# should check for date first and not pull data if it's the wrong date, to make backfilling faster
# TODO: find file using absolute paths

job_qualifications = [
    'Python', 'R ','AWS','Warehouse','Data Warehouse', 'Hive', 'Azure', 'Cloud', 'Java', 
    'C++', 'C ', 'Airflow', 'SQL', 'Database', 'Postgres', 'Machine Learning', 'Big Data',
     'ETL', 'Kafka', 'Apache Spark', 'PySpark', 'Scala','Terraform', 'Redshift','Pipeline', 'Hadoop',
     "Docker", "GitLab", "GitHub"
     ]

education = {
    "bachelor's degree": ["bachelor's", "bachelors degree"],
    "associate's degree": ["associate's", "associates degree"],
    "master's degree": ["master's degree", "masters degree"],
    "PhD": ["phd"]
    }

def find_keywords(df):
    """ Check for keywords and throw away the rest """
    df["responsibilities"] = df["responsibilities"].str.lower()
    df["basic_qualifications"] = df["basic_qualifications"].str.lower()
    df["preferred_qualifications"] = df["preferred_qualifications"].str.lower()
    df["education"] = df["education"].str.lower()
    df["preferred_education"] = df["preferred_education"].str.lower()
    df["key_qualifications"] = df["key_qualifications"].str.lower()
    return df


def create_csv(d, date_pulled=""):
    """ Creates a CSV from a dictionary, with naming convention "datepulled_disney.csv" """
    if type(d) == dict:
        disney_data = pd.DataFrame.from_dict(d, orient="index")
    else:
        try:
            disney_data = pd.read_csv(d)
        except:
            print("This isn't a dataframe")
        disney_data = find_keywords(disney_data)

    return disney_data.to_csv(f"{date_pulled}_disney.csv")


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
    create_csv(all_job_details_by_id, start_date)
    # upload_to_s3("disney.csv")

if __name__ == "__main__":
    # change for start date wanted
    main(start_date="")