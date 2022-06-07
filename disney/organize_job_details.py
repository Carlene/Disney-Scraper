####################### Standard Libraries #####################################
####################### My Libraries ###########################################
from scraper import grab_job_data_from_multiple_links
import filter_job_results as fjr

def separate_job_posts(list_of_jobs):
    """Separates job postings into necessary fields: job_id, job_path, job location, job title, job brand"""
    job_details_by_id = {}
    job_details = {}
    paths = []

    for job in list_of_jobs:
        if len(job) > 0:
            path = fjr.find_path(job)
            id = fjr.find_id(job)
            title = fjr.find_title(job)
            brand = fjr.find_brand(job)
            locations = fjr.find_locations(job)
            posting_date = fjr.find_posting_date(job)
            job_details["path"] = path
            job_details["title"] = title
            job_details["brand"] = brand
            job_details["locations"] = locations
            job_details["posting_date"] = posting_date
            job_details_by_id[id] = job_details
            job_details = {}
            paths.append(path)
    return job_details_by_id, paths


def job_qualifications(messy_descriptions_by_job_id):
    """Takes all filter functions and applies it to each inner job posting. 
    Splits up responsibilities, qualifications, education into a dictionary"""

    quals_by_job_id = {}
    clean_quals_by_type = {}
    
    for job_id, messy_descriptions in messy_descriptions_by_job_id.items():
        for messy_description in messy_descriptions:
            jobs_no_summary_by_job_id = fjr.replace_job_summary(messy_description)
            no_disney_description = fjr.remove_disney_company_description(jobs_no_summary_by_job_id)
            responsibilities = fjr.find_responsibilities(no_disney_description)
            basic_qualifications, preferred_qualifications = fjr.find_qualifications(no_disney_description)

            clean_quals_by_type["Responsibilities"] = responsibilities
            clean_quals_by_type["Basic Qualifications"] = basic_qualifications
            clean_quals_by_type["Preferred Qualifications"] = preferred_qualifications

            quals_by_job_id[job_id] = clean_quals_by_type
            clean_quals_by_type = {}
    return quals_by_job_id


def map_job_details_with_qualifications(list_of_jobs, job_id = ""):
    """Takes two lists of job data (without qualifications) and url of the actual job posting (to grab qualifications) and combines this data together  

    Outputs:
    all_job_details_by_id: a dictionary of all job details per id
    """
    all_job_details_by_id = {}
    job_details_by_id = separate_job_posts(list_of_jobs)[0]
    list_of_paths = separate_job_posts(list_of_jobs)[1]
    messy_descriptions_by_job_id = grab_job_data_from_multiple_links(list_of_paths)
    quals_by_job_id = job_qualifications(messy_descriptions_by_job_id)

    if job_id != "":
        all_job_details_by_id[job_id] = job_details_by_id[job_id] | quals_by_job_id[job_id]
        print(f"All job details after combining: {len(all_job_details_by_id)}")
        return all_job_details_by_id

    for id in job_details_by_id:
        if id in messy_descriptions_by_job_id:
            all_job_details_by_id[id] = job_details_by_id[id] | quals_by_job_id[id]
    print(f"All job details after combining: {len(all_job_details_by_id)}")
    return all_job_details_by_id