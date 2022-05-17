# Jobs come in HTML formatted list

def split_and_clean(HTML, element):
    """Turns the WebElement into a python list, removes unnecessary white space, and splits up job posting by HTML element (tr)"""
    jobs = ""
    for job in HTML:
        jobs += job.get_attribute('innerHTML')

    clean_jobs = jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    jobs = clean_jobs.split(element)
    return jobs