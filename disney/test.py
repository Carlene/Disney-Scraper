####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries ###########################################
from scraper import scrape_every_page
import organize_job_details as organize
################################################################################


def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    print(df.shape)
    return df.to_csv("disney.csv")

if __name__ == "__main__":
    pages = 3
    search_page_job_list = scrape_every_page(pages, "</tr>")
    all_job_details_by_id = organize.map_job_details_with_qualifications(search_page_job_list)
    create_csv(all_job_details_by_id)

