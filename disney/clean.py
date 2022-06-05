# Jobs come in HTML formatted list

def split_and_clean(HTML, element):
    """Turns a WebElement into a python list, removes unnecessary white space, and splits up the WebElement by a specific HTML element (for job postings, the tag is <tr>)"""
    jobs = ""
    for job in HTML:
        jobs += job.get_attribute('innerHTML')

    clean_jobs = jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    jobs = clean_jobs.split(element)
    return jobs

def many_split_and_clean(nested_list_of_web_elements, HTMLelement):
    """Goes through a list of lists of WebElements, turns it into a python list of lists, removes unnecessary white space, and splits up the WebElement by a specific HTML element (for job postings, the tag is <tr>)"""
    search_page_jobs = ""
    for list_of_web_elements in nested_list_of_web_elements:
        for web_element in list_of_web_elements:
            search_page_jobs += web_element.get_attribute('innerHTML')

    clean_jobs = search_page_jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    search_page_jobs = clean_jobs.split(HTMLelement)
    return search_page_jobs