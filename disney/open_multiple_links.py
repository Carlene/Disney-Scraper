####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
####################### My Libraries ###########################################
from scraper import split_and_clean
################################################################################

def add_disney_url(paths):
    """Concats the start of the url to the list of job paths"""
    full_links = []
    url_start = "https://jobs.disneycareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links


#TODO: count links and do something if count is off (15 a page)

description_div = "ats-description"

def grab_job_data_from_multiple_links(paths):
    """ 1. Opens a web browser (minimizes the window)
        2. Opens a specific job link 
        3. Grabs the HTML text where the job description is held
        4. Creates a list of details per job 
        5. Creates a mapping of all job details to job id of posting"""
    messy_descriptions_by_job_id = {}
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.minimize_window()
    urls = add_disney_url(paths)

    for url in urls:
        job_id = url.split("/", )[-1]
        driver.get(url)
        driver.implicitly_wait(10)
        job_description = driver.find_elements(By.CLASS_NAME, value=description_div)
        desc = split_and_clean(job_description, "<h2>")
        messy_descriptions_by_job_id[job_id] = desc
    driver.close()
    return messy_descriptions_by_job_id