###############################################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def find_description(posting):
    """The job description for Meta Jobs is the second item in the posting"""
    # TODO: OK, the job description is first, second, and a tiny bit of the third items. 
    # Need to grab [:3], then the first part of third index before </div>
    return posting[2]

def find_responsibilities_and_qualifications(posting, lookup_start, lookup_end):
    """Used to search for keywords in the body of the rest of the job posting to filter out qualifications vs. requirements"""
    job_details = [posting[4]]
    holder = []
    starting_paragraph = lookup_start
    ending_paragraph = lookup_end

    for detail in job_details:
        start_position = detail.find(starting_paragraph)
        end_position = detail.find(ending_paragraph)
        if start_position > -1 and end_position > -1:
            holder.append(detail[start_position : end_position])
    return holder


beginning = "Responsibilities"
middle = "Minimum"
end = "Locations"


def filter_posting(text):
    f = open(text)
    posting = f.readlines()

    descriptions = find_description(posting) #string
    responsibilities = find_responsibilities_and_qualifications(posting, beginning, middle) #list
    qualifications = find_responsibilities_and_qualifications(posting, middle, end) #list

    f.close()

    return descriptions, responsibilities, qualifications