from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
###############################################################
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


import scraper 
import find_urls
import open_job_links
import filter_job_posting
import pandas as pd

descriptions, responsibilities, qualifications = filter_job_posting.filter_posting(open_job_links.description_file)
print(responsibilities)