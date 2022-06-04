from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
###############################################################
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#TODO create a file that goes through each page of the job search (maybe also shows 100 jobs per page?)
def launchBrowser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.minimize_window()
    driver.get("https://jobs.disneycareers.com/search-jobs/data%20engineer/391-28648/1?glat=40.71427&glon=-74.00597")
    return driver

def scrape_HTML():
    driver = launchBrowser()
    job_list = driver.find_elements(By.TAG_NAME, value='tbody') #div class that holds job postings
    # driver.close()
    return job_list