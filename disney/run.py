####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries #####################################
from scraper import scrape_HTML
from clean import split_and_clean
import organize_job_details as organize
from open_multiple_links import grab_job_data_from_multiple_links
############################################################

# TODO: rename variables to better show the difference between details grabbed from the search page vs. the actual job posting
def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv("disney.csv")
    # return df

if __name__ == "__main__":
    job_elements = scrape_HTML()
    job_list = split_and_clean(job_elements, "</tr>")
    all_job_details_by_id = organize.map_job_details_with_qualifications(job_list)
    create_csv(all_job_details_by_id)