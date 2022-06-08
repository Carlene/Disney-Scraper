#######  Functions to filter job details pulled from the main job search page ####### 
#TODO: Do something if functions don't find anything
#TODO: Can maaaaybe refactor all the find functions into one function that different paramaters are given to, problem is they all have little tiny annoying differences

##############  Functions to filter job details from the main job search page ############## 
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

    posting_date = job[starting_i + len(posting_date_start) : ending_i]
    return posting_date

##############  Functions to filter job details from a specific job's page ############## 

# def replace_job_summary(job_description):
#     """Removes unecessary start of job description"""
#     look_for = "<h4>"

#     starting_i = job_description.find(look_for)
#     ending_i = job_description.find(look_for, starting_i + 1) # to start looking for header tags after the first one

#     job_summary = job_description[starting_i + len(look_for) : ending_i]

#     job_description_without_summary = job_description.replace(job_summary, "")
#     return job_description_without_summary


# def remove_disney_company_description(job_description):
#     "Removes tail of job description, which explains about the Disney company"
#     look_for = "<!--<h3>"

#     starting_i = job_description.find(look_for)

#     if starting_i < 0:
#         return job_description
#     else:
#         ending_i = len(job_description) # disney "about" lasts to the end of the description
#         about = job_description[starting_i : ending_i]
#         job_description_no_about = job_description.replace(about, "")
#     return job_description_no_about


#TODO: Need to completely rethink these functions, postings don't always use basic and preferred qualifications, 
# sometimes there's key qualifications. responsibilities will probably do the same thing
# Can maybe split on header h4, since that's usually a new category


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

# def find_responsibilities(job_description):
#     """ Separates out responsibilities from job posting """
#     responsibilities_start = "<h4>Responsibilities:</h4>"
#     responsibilities_end = "<h4>Basic Qualifications:</h4>"

#     starting_i = job_description.find(responsibilities_start)
#     if starting_i < 0:
#         responsibilities_start = "<h2>Responsibilities</h2>"
#         responsibilities_end = "<h2>Key Qualifications</h2>"
#         starting_i = job_description.find(responsibilities_start)
#         if starting_i < 0:
#             return job_description

#     ending_i = job_description.find(responsibilities_end) # to start looking for header tags after the first one
#     responsibilities = job_description[starting_i:ending_i]
#     return responsibilities



# def find_qualifications(job_description):
#     """ Separates out basic and preferred qualifications from job posting"""
#     basic_start = "<h4>Basic Qualifications:</h4>"
#     basic_end = "<h4>Preferred Qualifications:</h4>"
#     preferred_end = "<h4>Required Education</h4>"

#     starting_basic = job_description.find(basic_start)
#     starting_preferred_basic_end = job_description.find(basic_end)

#     if (starting_basic < 0) and (starting_preferred_basic_end < 0): 
#         return "not", "found"
#     else:
#         ending_preferred = job_description.find(preferred_end)
#         basic_qualifications = job_description[starting_basic:starting_preferred_basic_end]
#         preferred_qualifications = job_description[starting_preferred_basic_end:ending_preferred]
#         return basic_qualifications, preferred_qualifications


# def remove_job_summary(description_dict):
#     description_by_job_id = {}
#     descriptions_list = []
#     for id, desc in description_dict.items():
#         for item in desc:
#             desc_no_summary = replace_job_summary(item)
#             descriptions_list.append(desc_no_summary)
#         description_by_job_id[id] = descriptions_list
#         descriptions_list = []
#     return description_by_job_id