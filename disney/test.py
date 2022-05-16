from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
###############################################################
from selenium.webdriver.common.by import By

link = "https://docs.google.com/presentation/u/0/"
link2 = "https://sheets.google.com"
link3 = "https://docs.google.com"
# link4 = "https://google.com"

links = []
links.extend([link, link2, link3])

def launchBrowser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.minimize_window()
    holder = []
    for url in links:
        driver.get(url)
        html_source = driver.page_source
        holder.append(html_source)
    driver.close()
    return holder

print(launchBrowser())