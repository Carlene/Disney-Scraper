####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
####################### My Libraries #####################################
from clean import split_and_clean

def add_disney_url(paths):
    """Concats the start of the url to the list of job paths"""
    full_links = []
    url_start = "https://jobs.disneycareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links

def find_job_id_in_url(url):
    job_id = url.split("/", )[-1]
    return job_id

#TODO: count links and do something if count is off (15 a page)

description_div = "ats-description"

def grab_job_data_from_multiple_links(paths):
    """Creates a mapping of all job details (not separated yet) to job id of posting"""
    description_by_job_id = {}
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.minimize_window()
    urls = add_disney_url(paths)

    for url in urls:
        job_id = find_job_id_in_url(url)
        driver.get(url)
        job_description = driver.find_elements(By.CLASS_NAME, value=description_div)
        desc = split_and_clean(job_description, "<h2>")
        description_by_job_id[job_id] = desc
    driver.close()
    return description_by_job_id