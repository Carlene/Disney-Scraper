from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
###############################################################
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def launchBrowser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.metacareers.com/jobs/?q=data")
    return driver

driver = launchBrowser()
continue_link = driver.find_element(By.CLASS_NAME, value='_8tk7') #div class that holds job postings
innerHTMLpls = continue_link.get_attribute('innerHTML') 

#TODO hide your fucking path name jesus christ
with open('C:\\Users\\Lene\\Documents\\DS4A\\DS4ADataEngineering\\job_scraper\\raw_data\\source_holder.txt', 'a+') as f:
    f.write(innerHTMLpls)
    f.close
