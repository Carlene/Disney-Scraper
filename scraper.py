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
    driver.get("https://www.metacareers.com/jobs/?q=data")
    return driver

def main():
    driver = launchBrowser()
    continue_link = driver.find_element(By.CLASS_NAME, value='_8tk7') #div class that holds job postings
    innerHTMLpls = continue_link.get_attribute('innerHTML') 

    with open('source_holder.txt', 'a+') as f:
        f.write(innerHTMLpls)
        f.close
