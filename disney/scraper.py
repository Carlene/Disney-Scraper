####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
####################### My Libraries ###########################################
################################################################################

#TODO create a file that goes through each page of the job search (maybe also shows 100 jobs per page?)
def launchBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options= options, service=Service(ChromeDriverManager().install()))
    # driver.minimize_window()
    driver.get("https://jobs.disneycareers.com/search-jobs/data%20engineer/391-28648/1?glat=40.71427&glon=-74.00597")
    return driver


def split_and_clean(list_of_web_elements, HTMLelement):
    """Goes through a list of lists of WebElements, turns it into a python list of lists, removes unnecessary white space, and splits up the WebElement by a specific HTML element (for job postings, the tag is <tr>)"""
    search_page_jobs = ""
    for web_element in list_of_web_elements:
        search_page_jobs += web_element.get_attribute('innerHTML')

    clean_jobs = search_page_jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    search_page_jobs = clean_jobs.split(HTMLelement)
    return search_page_jobs


def scrape_every_page(pages, HTMLelement):
    """ 1. Opens Data Engineer search page and maximizes window
        2. Clicks the x on the cookie warning pop up, if there
        3. Looks for tag that holds HTML high level job posting data on the search page and puts that data into a web element list
        4. Cleans the white space and some of the tags to put each job data as an item in a list
        5. Stops when there are no more pages to go through
         """
    driver = launchBrowser()
    driver.maximize_window()

    search_page_job_list = []
    while pages > 0: 
        try:
            button = driver.find_element_by_id("onetrust-close-btn-container") # id that closes the cookie pop up
            button.click() # clicking the x on the pop up
        except:
            print(f"Cookie pop up isn't there.")
        driver.implicitly_wait(10)
        web_element_jobs = driver.find_elements(By.TAG_NAME, value='tbody') # tag that holds job postings info
        search_page_job_list += split_and_clean(web_element_jobs, HTMLelement) 
        next = driver.find_element(By.LINK_TEXT, value='Next') # text that holds next page info
        driver.execute_script("arguments[0].click();", next) # clicking the next button using javascript
        pages -= 1
    return search_page_job_list

    