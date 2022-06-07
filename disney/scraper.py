####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
####################### My Libraries ###########################################
################################################################################

def launchBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options= options, service=Service(ChromeDriverManager().install()))
    # driver.minimize_window()
    driver.get("https://jobs.disneycareers.com/search-jobs/data%20engineer/391-28648/1?glat=40.71427&glon=-74.00597")
    return driver


def split_and_clean(list_of_web_elements, HTMLelement):
    """ 1. Goes through a list of lists of WebElements
        2. Turns it into a python list of lists, removes unnecessary white space
        3. Splits up the WebElement by a specific HTML element (for job postings, the tag is <tr>)
        """
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
    print(f"Jobs found: {len(search_page_job_list)}")
    return search_page_job_list


def add_disney_url(paths):
    """Concats the start of the url to the list of job paths"""
    full_links = []
    url_start = "https://jobs.disneycareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links


# TODO: count links and do something if count is off (15 a page)
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
        # driver.implicitly_wait(10) # pls wait until the elements are found ty
        job_description = driver.find_elements(By.CLASS_NAME, value=description_div)
        desc = split_and_clean(job_description, "<h2>")
        messy_descriptions_by_job_id[job_id] = desc
    print(f"Amount of job ids with job details kept: {len(messy_descriptions_by_job_id)}")
    return messy_descriptions_by_job_id