####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
####################### My Libraries #####################################
from clean import split_and_clean
###############################################################

#TODO create a file that goes through each page of the job search (maybe also shows 100 jobs per page?)
def launchBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options= options, service=Service(ChromeDriverManager().install()))
    # driver.minimize_window()
    driver.get("https://jobs.disneycareers.com/search-jobs/data%20engineer/391-28648/1?glat=40.71427&glon=-74.00597")
    return driver

# def scrape_HTML():
#     driver = launchBrowser()
#     job_list = driver.find_elements(By.TAG_NAME, value='tbody') #div class that holds job postings
#     return job_list

def scrape_HTML():
    """ Scrapes job information from the search page includin url, title, location and posting date"""
    driver = launchBrowser()
    job_list = driver.find_elements(By.TAG_NAME, value='tbody') #div class that holds job postings
    return job_list

def scrape_every_page(pages):
    """Will grab a list of jobs links """
    driver = launchBrowser()
    driver.maximize_window()
    driver.implicitly_wait(10)

    job_list = []
    while pages > 0:
        job_list.append(driver.find_elements(By.TAG_NAME, value='tbody')) # tag that holds job postings info
        try:
            button = driver.find_element_by_id("onetrust-close-btn-container") # id that closes the cookie pop up
            button.click() # clicking the x on the pop up
        except:
            print("Cookie pop up isn't there")
        next = driver.find_element(By.LINK_TEXT, value='Next') # text that holds next page info
        driver.execute_script("arguments[0].click();", next) # clicking the next button using javascript
        pages -= 1
    return job_list

    