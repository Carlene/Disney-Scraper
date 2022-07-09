####################### Standard Libraries #####################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
####################### My Libraries ###########################################
from filter_job_results import find_in_description
################################################################################
######################## Use Case ##############################################
"""
Holds scripts that launch a browser, and wanders through the Disney search page and job postings pages
"""
################################################################################

def launch_browser(url):
    options = webdriver.ChromeOptions()
    # bug with chrome=103.0.5060.66, trying with beta
    options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
    options.add_experimental_option("detach", True) # chromedriver closes without this option
    driver = webdriver.Chrome(options= options, service=Service(ChromeDriverManager(version='104.0.5112.20').install()))
    driver.minimize_window()
    driver.get(url)
    return driver

# TODO: combine the part of scrape every page where i look for the job posting holder info 
# TODO: make wait a variable to change all implicit waits
def split_and_clean(list_of_web_elements, HTMLelement=''):
    """ 1. Goes through a list of lists of WebElements on the job search page
        2. Turns it into a python list of lists, removes unnecessary white space
        3. Splits up the WebElement by a specific HTML element (for job postings, the tag is <tr>)
        """
    search_page_jobs = ""

    if HTMLelement == "": # we're within a job posting
        for web_element in list_of_web_elements:
            web_element = web_element.text.replace("\n", " ")
            search_page_jobs += web_element
        return search_page_jobs
    else: #we're on the main job search page
        for web_element in list_of_web_elements:
            search_page_jobs += web_element.get_attribute('innerHTML')

    clean_jobs = search_page_jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    search_page_jobs = clean_jobs.split(HTMLelement)
    return search_page_jobs


def scrape_every_page(pages = "", HTMLelement = '</tr>'):
    """ 1. Opens Data Engineer search page and maximizes window
        2. Clicks the x on the cookie warning pop up, if there
        3. Looks for tag that holds HTML high level job posting data on the search page and puts that data into a web element list
        4. Cleans the white space and some of the tags to put each job data as an item in a list
        5. Stops when there are no more pages to go through
         """
    url = "https://jobs.disneycareers.com/search-jobs/data%20engineer/"
    driver = launch_browser(url)
    count = 0
    # class that holds amount of pages within job search. text is "of [number]"
    if pages == "":
        pages = driver.find_element(By.CLASS_NAME, value='pagination-total-pages') 
        pages = int(pages.text[-2:])
        
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

        try:
            next = driver.find_element(By.LINK_TEXT, value='Next') # text that holds next page info
            driver.execute_script("arguments[0].click();", next) # clicking the next button using javascript
        except:
            print("Next button isn't there")

        pages -= 1
        count += 1
        print(f"{count} down, {pages} pages to go!:D")
        time.sleep(2) # don't want to upset the mouse
    print(f"Jobs found: {len(search_page_job_list)}")
    return search_page_job_list


def add_disney_url(paths):
    """Concats the start of the url to the list of job paths"""
    full_links = []
    url_start = "https://jobs.disneycareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links


def grab_job_data_from_multiple_links(paths):
    """ 1. Opens a web browser (minimizes the window)
        2. Opens a specific job link 
        3. Grabs the HTML text where the job description is held, and cleans it, and turns it into a string
        4. Splits up different parts of the job description into education, qualifications, etc.
        4. Creates a list of job description details per job 
        5. Creates a mapping of all job details to job id of posting"""
    post_descriptions_by_job_id = {}
    driver = launch_browser("https://jobs.disneycareers.com")
    driver.minimize_window()
    urls = add_disney_url(paths)
    jobs_gotten_through = 1
    all_jobs_count = len(urls)

    for url in urls:
        job_id = url.split("/", )[-1]
        driver.get(url)
        driver.implicitly_wait(10) # pls wait until the elements are found ty
        job_description = driver.find_elements(By.CLASS_NAME, value="ats-description")
        desc = split_and_clean(job_description)
        # filter out text that's actually needed
        responsibilities = find_in_description(desc, "Responsibilities", "Qualifications")
        basic_qualifications = find_in_description(desc, "Basic Qualifications", "Preferred Qualifications")
        preferred_qualifications = find_in_description(desc, "Preferred Qualifications", "Required Education")
        education = find_in_description(desc, "Required Education", "Additional Information")
        preferred_education = find_in_description(desc, "Preferred Education", "Additional Information")
        key_qualifications = find_in_description(desc, "Key Qualifications", "Nice To Haves")
        nice_to_haves = find_in_description(desc, "Nice To Haves", "Additional Information")
        what_to_do = find_in_description(desc, "WHAT YOU'LL DO", "WHAT TO BRING")
        what_to_bring = find_in_description(desc, "WHAT TO BRING", "About")
        experience = find_in_description(desc, "We're looking for candidates with experience in the following areas:", "To be considered for a Lead position on the team, you must demonstrate the following:")
        lead_experience = find_in_description(desc, "To be considered for a Lead position on the team, you must demonstrate the following:", "Required Education")
        #and put it all together
        post_descriptions_by_job_id[job_id] = {
            "responsibilities" : responsibilities + " " + what_to_do,
            "basic_qualifications" : basic_qualifications + " " + experience,
            "preferred_qualifications" : preferred_qualifications + " " + lead_experience,
            "education" : education + " " + what_to_bring,
            "preferred_education" : preferred_education,
            "key_qualifications" : key_qualifications,
            "nice_to_haves" : nice_to_haves
            }
        print(f"Gotten through {jobs_gotten_through} jobs, {all_jobs_count} to go!") # print a checkup 
        jobs_gotten_through +=1
        all_jobs_count -= 1
    print(f"Amount of job ids with job details kept: {len(post_descriptions_by_job_id)}")
    return post_descriptions_by_job_id