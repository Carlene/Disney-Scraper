####################### Standard Libraries #####################################
import pandas as pd
from selenium.webdriver.common.by import By
####################### My Libraries ###########################################
from scraper import launch_browser, scrape_every_page
from filter_job_results import find_in_description
from organize_job_details import separate_job_posts, grab_job_data_from_multiple_links, map_job_details_with_qualifications
###############################################################################


url = "https://jobs.disneycareers.com/job/santa-monica/data-analyst/391/17798057824"
driver = launch_browser(url)
inner_date = driver.find_element(By.TAG_NAME, value="job-date job-info") 
print(inner_date.text)
