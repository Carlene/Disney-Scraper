from scraper import write_HTML_to_file
from scraper import scrape_HTML
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
    # save_file = open('source_holder.txt', "r+") 
    # job_data = scraper.scrape_HTML(scraper.launchBrowser(), save_file)
    job_data = write_HTML_to_file(scrape_HTML())
    print(job_data)
    # paths = find_urls.grab_job_paths(job_data)
    # links = find_urls.add_meta_url(paths)
    # print(links)
    # open_job_links.grab_job_data_from_multiple_links(links[:3])
    # descriptions, responsibilities, qualifications = filter_job_posting.filter_posting(open_job_links.description_file)
    # print(descriptions)
    # print(responsibilities)
    # print(qualifications)
    # job_data.seek(0)
    # job_data.truncate(0)
    # job_data.close()