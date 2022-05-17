####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries #####################################
from scraper import scrape_HTML
from clean import split_and_clean
import organize_job_details as organize
from open_multiple_links import grab_job_data_from_multiple_links
from filter_job_results import separate
############################################################

def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    # df.to_csv("disney.csv")
    return df

if __name__ == "__main__":
    job_elements = scrape_HTML()
    job_list = split_and_clean(job_elements, "</tr>")
    paths = separate(job_list)[1]
    print(organize.job_qualifications(grab_job_data_from_multiple_links(paths)))

    # create_csv(job_details_by_id)
    # df = create_csv(job_details_by_id)
    # print(df)
    # organize.map_job_details_with_qualifications(job_list)