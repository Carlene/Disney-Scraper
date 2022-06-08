####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries ###########################################
from scraper import scrape_every_page
import organize_job_details as organize
################################################################################

# TODO: make job dictionary keys into tuples with job posting date and job id
# TODO: aggressively filter out postings without Data or Engineer
# TODO: find file using absolute paths

def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv("disney.csv")

if __name__ == "__main__":
    pages = 2
    search_page_job_list = scrape_every_page(pages)
    all_job_details_by_id = organize.map_job_details_with_qualifications(search_page_job_list)
    create_csv(all_job_details_by_id)