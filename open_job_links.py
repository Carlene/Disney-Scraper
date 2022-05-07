"""My code"""
from find_urls import grab_job_paths 
from find_urls import add_meta_url
###############################################################
"""Other libraries"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def launchBrowser(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.minimize_window()
    driver.get(link)
    return driver


def grab_job_data(driver, div_class, save_file):
    continue_link = driver.find_element(By.CLASS_NAME, value=div_class) #div class that holds all job locations
    innerHTMLpls = continue_link.get_attribute('innerHTML') 

    with open(save_file, 'a+', encoding="utf-8") as f:
        f.write(innerHTMLpls)
        f.close

    print("done")


location_div = '_9atc'
description_div = '_8muv'
locations_file = 'locations.txt'
description_file = 'description.txt'

def grab_job_data_from_multiple_links(links):
    for link in links:
        driver = launchBrowser(link)
        grab_job_data(driver, location_div, locations_file)
        grab_job_data(driver, description_div, description_file)
        driver.close()