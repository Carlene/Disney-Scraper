###############################################################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def grab_description(posting):
    """The job description for Meta Jobs is the second item in the posting"""
    return posting[2]

def grab_responsibilities_and_qualifications(posting, lookup_start, lookup_end):
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

def grab_responsibilities(posting):
    starting_paragraph = "Responsibilities"
    ending_paragraph = "Minimum"
    responsibilities = grab_responsibilities_and_qualifications(posting, starting_paragraph, ending_paragraph)
    return responsibilities

def grab_qualifications(posting):
    starting_paragraph = "Minimum"
    ending_paragraph = "Locations"
    qualifications = grab_responsibilities_and_qualifications(posting, starting_paragraph, ending_paragraph)
    return qualifications

def main(text):
    f = open(text)
    posting = f.readlines()

    description = grab_description(posting) #string
    responsibilities = grab_responsibilities(posting) #list
    qualifications = grab_qualifications(posting) #list

    f.close()

    return description, responsibilities, qualifications