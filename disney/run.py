####################### Standard Libraries #####################################
import pandas as pd
####################### My Libraries #####################################
from scraper import scrape_HTML
from filter_job_results import separate
from clean import split_and_clean
from open_multiple_links import add_disney_url
from open_multiple_links import grab_job_data_from_multiple_links
############################################################

def create_csv(d):
    df = pd.DataFrame.from_dict(d, orient="index")
    # df.to_csv("disney.csv")
    return df

if __name__ == "__main__":
    job_elements = scrape_HTML()
    job_list = split_and_clean(job_elements, "</tr>")
    job_details_by_id = separate(job_list)[0]
    paths = separate(job_list)[1]
    links = add_disney_url(paths)
    job_data = grab_job_data_from_multiple_links(links)
    # create_csv(job_details_by_id)
    # df = create_csv(job_details_by_id)
    # print(df)
    print(job_data)