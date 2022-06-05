####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries #####################################
from scraper import scrape_HTML, scrape_every_page
from clean import split_and_clean, many_split_and_clean
import organize_job_details as organize
from open_multiple_links import grab_job_data_from_multiple_links
############################################################

def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    return df.to_csv("disney.csv")
    # return df

if __name__ == "__main__":
    pages = 3
    job_elements = scrape_every_page(pages)
    search_page_jobs = many_split_and_clean(job_elements, "</tr>")
    all_job_details_by_id = organize.map_job_details_with_qualifications(search_page_jobs)
    create_csv(all_job_details_by_id)

"""1. Open first browser with data engineer search
    2. Grab list of job posting urls and location/title/id/posting date info
    3. Open second browser 
    4. Go through list of job urls to grab data
    5. Append data to a df
    6. Close second browser (?)
    7. Go to first browser and click next page
    8. Steps 2 - 7 until gone through all pages
    9. Create csv with completed dataframe"""

"""1. Open first browser with data engineer search
    2. Grab list of job posting urls and location/title/id/posting date info
    3. Click next page
    4. Step 2 -3 til gone through all pages and have a list of job urls and job search data
    5. Go through list of job urls to grab data
    6. Append data to a df
    7. Create csv with completed dataframe"""