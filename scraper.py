from numpy import save
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
    driver.get("https://careers.crocs.com/careers/default.aspx")
    return driver

def write_HTML_to_file(HTML, save_file):
    f = open(save_file, "a+") 
    f.write(HTML)
    job_data = f.readlines()
    return job_data
    # with open(save_file, 'r+') as f:
    #     f.write(HTML)
    #     f.close()

def scrape_HTML(driver, save_file):
    driver = launchBrowser()
    continue_link = driver.find_element(By.CLASS_NAME, value='module_items-container') #div class that holds job postings
    innerHTMLpls = continue_link.get_attribute('innerHTML') 
    write_HTML_to_file(innerHTMLpls, save_file)


