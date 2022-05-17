from scraper import scrape_HTML
from filter_job_results import separate
from clean import split_and_clean
from open_multiple_links import grab_job_data_from_multiple_links
import filter_job_results as fjr

#TODO pull job details from links

def map_job_details_with_qualifications(urls, jobs):
    grab_job_data_from_multiple_links(urls)
    job_details_by_id = separate(jobs)[0]