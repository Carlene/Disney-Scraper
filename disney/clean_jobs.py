from scraper import scrape_HTML

# Jobs come in HTML formatted list

def split_and_clean(HTML_job_list):
    jobs = ""
    for job in HTML_job_list:
        jobs += job.get_attribute('innerHTML')

    clean_jobs = jobs.replace("\n", "")
    clean_jobs = " ".join(clean_jobs.split())
    jobs = clean_jobs.split("</tr>")
    return jobs

# Separating all of the information I need by formatting used in the HTML 

def find_id(job):
    id_start = "data-job-id="
    id_end = "<h2>"

    starting_i = job.find(id_start) 
    ending_i = job.find(id_end) 
    id = job[starting_i + len(id_start) : (ending_i- 2)] # subratracing two from ending id to get rid of "> "
    return id

def find_link(job):
    link_start = "a href="
    link_end = "data-job-id="

    starting_i = job.find(link_start)
    ending_i = job.find(link_end)

    link = job[starting_i + len(link_start) : ending_i]
    return link

def find_title(job):
    title_start = "<h2>"
    title_end = "</h2>"

    starting_i = job.find(title_start)
    ending_i = job.find(title_end)

    title = job[starting_i + len(title_start) : ending_i]
    return title

def find_brand(job):
    brand_start = "job-brand industry"
    brand_end = "</span>"

    starting_i = job.find(brand_start)
    ending_i = job.find(brand_end, starting_i+1) # to start looking for spans after the brand start

    brand = job[starting_i + len(brand_start) : ending_i]
    return brand


def separate(jobs):
    d = {}
    d2 = {}

    for job in jobs:
        link = find_link(job)
        id = find_id(job)
        title = find_title(job)
        brand = find_brand(job)
        d2["link"] = link
        d2["title"] = title
        d2["brand"] = brand
        d[id] = d2
        d2 = {}

    return d

# output:
# {
#   job_id:{
#      link:link, 
#      title:data engineer, 
#      date_posted:date, 
#      brand:company, 
#      location:[] 
#   },
#   job_id:{
#   }
# }