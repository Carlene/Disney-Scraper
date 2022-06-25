####################### Standard Libraries #####################################
from datetime import datetime as dt
####################### Use Case ###############################################
"""
Holds scripts that filter job data from the main job search page and within job postings
"""
################################################################################

########  Functions to filter job details from the main job search page ########
#TODO: Do something if functions don't find anything
#TODO: Can maaaaybe refactor all the find functions into one function that different parameters are given to, problem is they all have little tiny annoying differences

def find_id(job):
    """Finds the job posting id for reference"""
    id_start = "data-job-id="
    id_end = "<h2>"

    starting_i = job.find(id_start) 
    ending_i = job.find(id_end) 
    id = job[starting_i + len(id_start) : (ending_i- 2)] # subratracing two from ending id to get rid of "> "
    id = id.replace("\"", "")
    return id

def find_path(job):
    """Finds the path to the job posting"""
    path_start = "a href="
    path_end = "data-job-id="

    starting_i = job.find(path_start) +1 #to get rid of leading "
    ending_i = job.find(path_end) -2 #to get rid of " and whitespace

    path = job[starting_i + len(path_start) : ending_i]
    return path

def find_title(job):
    """Finds the title of the position the job posting is for"""
    title_start = "<h2>"
    title_end = "</h2>"

    starting_i = job.find(title_start)
    ending_i = job.find(title_end)

    title = job[starting_i + len(title_start) : ending_i]
    return title

def find_brand(job):
    """Finds the specific Disney Org that this job posting is under (eg. ESPN, Disney Streaming Services, etc)"""
    brand_start = "job-brand industry"
    brand_end = "</span>"

    starting_i = job.find(brand_start) + 2 # to avoid " and >
    ending_i = job.find(brand_end, starting_i) # to start looking for spans after the brand start

    brand = job[starting_i + len(brand_start) : ending_i]
    return brand

def find_locations(job):
    """Finds location inside job posting. Job locations are formatted as City, State, Country"""
    location_start = "job-location"
    location_end = "</span>"

    starting_i = job.find(location_start) + 2 #to avoid " and >
    ending_i = job.find(location_end, starting_i) # to start looking for spans after the location start

    location = job[starting_i + len(location_start) : ending_i]

    locations = location.split("/") #multiple locations in HTML split up by a backslash
    return locations

def find_posting_date(job):
    """Finds the day that this job posting was added to the Disney Jobs site"""
    posting_date_start = "job-date-posted"
    posting_date_end = "</span>"

    starting_i = job.find(posting_date_start) + 2 #to avoid " and >
    ending_i = job.find(posting_date_end, starting_i+1) # to start looking for spans after the brand start

    date_str = job[starting_i + len(posting_date_start) : ending_i]
    # convert string to date for future comparison
    try:
        posting_date = dt.strptime(date_str, '%b. %d, %Y').date() # sometimes comes in as Jun. 3, 2022
    except ValueError:
        try:
            posting_date = dt.strptime(date_str, '%B %d, %Y').date() # but also sometimes comes in as May 3, 2022
        except Exception as e:
            print(e)
    return posting_date


##############  Functions to filter job details from a specific job's page ###############

# TODO: there are still american edge cases but i'm mostly missing details from non-american postings

def find_in_description(job:str, starting_str:str, ending_str:str):
    """ Takes in a starting and ending string to look for within a job description, 
    and grabs the part of the description between those strings """

    starting_i = job.find(starting_str) 
    if starting_i == -1:
        return "NA"
    ending_i = job.find(ending_str) 
    if ending_i == -1:
        # education has a few ways of ending across postings
        if "Education" in starting_str:
            ending_i = job.find("This role is considered") 
            if ending_i == -1:
                ending_i = job.find("About Disney Streaming:")
                if ending_i == -1:
                    return "NA"
        # qualifications also has a few ways of ending across postings
        elif "Qualifications" in starting_str:
            ending_i = job.find("Additional Information:")
            if ending_i == -1:
                 return "NA"
        # give up/another edge case
        else:
            return "NA"
    id = job[starting_i + len(starting_str) : ending_i] 
    return id