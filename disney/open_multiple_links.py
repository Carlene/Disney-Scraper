from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from scraper import scrape_HTML
from clean_jobs import separate
from clean_jobs import split_and_clean

def add_disney_url(paths):
    """Concats the start of the url to the list of job paths"""
    full_links = []
    url_start = "https://jobs.disneycareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links

#TODO: count links and do something if count is off (15 a page)

description_div = "ats-description"
# description_file = 'description.txt'

def grab_job_data_from_multiple_links(urls):
    description_holder = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.minimize_window()
    for link in urls:
        driver.get(link)
        job_description = driver.find_elements(By.CLASS_NAME, value=description_div)
        description_holder.append(job_description)
    driver.close()
    return description_holder