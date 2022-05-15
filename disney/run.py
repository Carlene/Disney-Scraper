from scraper import scrape_HTML
from clean_jobs import separate
from clean_jobs import split_and_clean
import pandas as pd

# Open Chrome, search for "data" on Meta Jobs site
# Will give list of jobs that each have a different url, so scrape list of urls from this page 
    # TBA: keep looping until you get 25, default # per page)
    # TBA: Click next page, scrape next page of urls
# Open each url, and grab job desc/location/qualifications/responsibilities
    # TBA: Clean quals/resps more
# TBA: Put that into a dataframe to eventually create a CSV

def concat_job_details():
    pass

def create_csv():
    pass


if __name__ == "__main__":
    job_data = scrape_HTML()
    jobs = split_and_clean(job_data)
    print(separate(jobs))