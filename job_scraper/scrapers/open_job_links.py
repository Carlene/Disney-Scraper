###############################################################
"""My code"""
from find_urls import check_for_jobs 
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
    driver.get(link)
    return driver

def main():
    list = add_meta_url(check_for_jobs()[1])
    driver = launchBrowser(list[1])

    """This is to grab job location"""
    #TODO: Sometimes jobs come as multiple locations, sometimes it comes as a single location. Have to account for that in future script
    continue_link = driver.find_element(By.CLASS_NAME, value='_97fe _6hy-') #div class that holds all job locations
    innerHTMLpls = continue_link.get_attribute('innerHTML') 
    print(innerHTMLpls) 

    with open('job_source_holder.html', 'a+') as f:
        f.write(innerHTMLpls)
        f.close

    """This is to grab job details"""
    continue_link = driver.find_element(By.CLASS_NAME, value='_8muv') #div class that holds all job details
    innerHTMLpls = continue_link.get_attribute('innerHTML') 
    print(innerHTMLpls)

    with open('job_source_holder.html', 'a+') as f:
        f.write(innerHTMLpls)
        f.close