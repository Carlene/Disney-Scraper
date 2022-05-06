###############################################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

f = open('description.txt') 
descriptions = f.readlines()

for description in descriptions:
    print(description)
    print("\n")

