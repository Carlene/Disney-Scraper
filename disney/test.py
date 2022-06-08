####################### Standard Libraries #####################################
import pandas as pd
from selenium.webdriver.common.by import By
####################### My Libraries ###########################################
from scraper import launch_browser, scrape_every_page
from filter_job_results import find_in_description
from organize_job_details import separate_job_posts, grab_job_data_from_multiple_links
################################################################################

# search_page_job_list = []
# # HTMLelement = ""
# url = "https://jobs.disneycareers.com/job/new-york/data-analyst/391/28818903776" # not found with scraper
# # # url = "https://jobs.disneycareers.com/job/new-york/sr-data-engineer/391/28413716960" # found with scraper
# driver = launch_browser(url)

# web_element_jobs = driver.find_elements(By.CLASS_NAME, value='ats-description')
# for web_element in web_element_jobs:
#     print(web_element)
#     search_page_job_list.append(web_element.text)
#     print(search_page_job_list)

# for job in search_page_job_list:
#     responsibilities = find_in_description(job, "Responsibilities:", "Qualifications")
#     basic_qualifications = find_in_description(job, "Basic Qualifications:", "Preferred Qualifications:")
#     preferred_qualifications = find_in_description(job, "Preferred Qualifications:", "Required Education")
#     education = find_in_description(job, "Required Education", "Additional Information:")
#     preferred_education = find_in_description(job, "Preferred Education", "Additional Information:")
#     key_qualifications = find_in_description(job, "Key Qualifications", "Nice To Haves")
#     nice_to_haves = find_in_description(job, "Nice To Haves", "Additional Information:")
#     print(responsibilities)

if __name__ == "__main__":
    pages = 2
    search_page_job_list = scrape_every_page(pages)
    job_details_by_id, paths = separate_job_posts(search_page_job_list)
    messy_descriptions_by_job_id = grab_job_data_from_multiple_links(paths)
    # all_job_details_by_id = organize.map_job_details_with_qualifications(search_page_job_list)
    # create_csv(all_job_details_by_id)
    # print(search_page_job_list)
    # print("\n")
    # print("\n")
    # print(job_details_by_id)
    # print("\n")
    # print("\n")
    print(messy_descriptions_by_job_id)