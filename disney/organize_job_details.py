from open_multiple_links import grab_job_data_from_multiple_links
import filter_job_results as fjr

def job_qualifications(description_by_job_id):
    no_summary_by_job_id = fjr.remove_job_summary(description_by_job_id)
    return no_summary_by_job_id

def map_job_details_with_qualifications(list_of_jobs):
    """Takes two lists of job data (without qualifications) and url of the actual job posting (to grab qualifications) 
    and combines this data together  

    Arguments (what it says on the tin):
    list_of_paths
    list_of_jobs

    Outputs:
    all_job_details_by_id: a dictionary of all job details per id
    """
    all_job_details_by_id = {}
    job_details_by_id = fjr.separate(list_of_jobs)[0]
    list_of_paths = fjr.separate(list_of_jobs)[1]
    quals_by_id = grab_job_data_from_multiple_links(list_of_paths)

    for id in job_details_by_id:
        if id in quals_by_id:
            all_job_details_by_id[id] = job_details_by_id[id]

            all_job_details_by_id[id].append(quals_by_id[id])
            print(all_job_details_by_id)
    # return all_job_details_by_id
    # return job_details_by_id, list_of_paths, quals_by_id