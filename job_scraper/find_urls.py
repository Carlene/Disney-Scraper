#TODO hide full path name 
f = open('source_holder.txt') 
split_up = f.readlines()
job_url = "/v2/jobs/"

link_holder = []

# TODO: Continue looping through this function until I get the correct amount of jobs (getting 14, should be 25) 
# Since "find" stops at the first instance of finding a substring, have to keep looping until there's no more new jobs

def check_for_jobs():
    """ Used to find job links within the Meta Job Search page source"""
    job_counter = 0
    for line in split_up:
        if line.find(job_url) > -1:
            job_counter+=1
            link_start = line.find(job_url)
            link_end = line.find("/", link_start+ len(job_url)) #making sure to grab the end of the job url
            link_holder.append(line[link_start : link_end])
    return job_counter, link_holder

def add_meta_url(paths):
    full_links = []
    url_start = "https://www.metacareers.com"
    for path in paths:
        full_links.append(url_start + path)
    return full_links

print(add_meta_url(check_for_jobs()[1]))
# def main():
#     check_for_jobs()
