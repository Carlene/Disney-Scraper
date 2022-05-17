from filter_job_results import separate
from open_multiple_links import grab_job_data_from_multiple_links
import filter_job_results as fjr

def map_job_details_with_qualifications(urls, jobs):
    all_job_details_by_id = {}
    job_details_by_id = separate(jobs)[0]
    quals_by_id = grab_job_data_from_multiple_links(urls)
    for id in job_details_by_id:
        if id in quals_by_id:
            all_job_details_by_id[id] = job_details_by_id[id]
            all_job_details_by_id[id].append(quals_by_id[id])
    return all_job_details_by_id