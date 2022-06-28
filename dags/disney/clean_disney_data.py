import pandas as pd
import ast
############################  FILTER DATAFRAME AT END #############################

def create_csv(data, file_string="", date_pulled=""):
    """ 
    When given a dictionary, creates a CSV file from the data (pretty unclean data from disney) named
    When given a CSV path, turns it into a df, applies more filtering functions, and only returns necessary columns to create a CSV file for Redshift
    """
    if isinstance(data, dict): # just give us everything 
        disney_data = pd.DataFrame.from_dict(data, orient="index")
        file_string = f"raw_{date_pulled}_disney.csv"
        disney_data.to_csv(file_string)
    elif isinstance(data, pd.DataFrame): # when splitting up raw df to locations/educations/etc dfs
        disney_data = data
        file_string+=f"{date_pulled}_disney.csv"
        disney_data.to_csv(file_string)
        
    print(disney_data.head())
    print("All done!")
    return disney_data


job_qualifications = [
    'Python', 'R ', 'AWS', ' Warehouse', 'Data Warehouse', 'Hive', 'Azure', 'Cloud', 'Java', 'C++', 'C ', 
    'Airflow', 'SQL', 'Database', 'Postgres', 'Machine Learning', 'Big Data', 'ETL', 'Kafka', 'Spark', 'Scala',
    'Terraform', 'Redshift', 'Pipeline', 'Hadoop', 'Docker', 'GitLab', 'GitHub', 'Kubernetes', 'HCI', 'Linux', 
    'OSX', 'svn', 'Gradle', 'Maven', 'Swift', 'Matlab', 'MongoDB', 'Objective-C', 'Ruby', 'Perl', 'Pig', 'Hadoop',
    'Cosmos', 'Javascript']

education = {
    "bachelor's degree": ["B.S", "BS in", "bachelor"],
    "associate's degree": ["associate's", "associates"],
    "master's degree": ["master's", "masters", "M.S", "MS in"],
    "PhD": ["phd", "doctorate", "ph.d"]
    }


def match_education(row):
    """ check if the row contains any mention of a degree keyword"""
    degree_list = []
    for degree, keywords in education.items():
        for keyword in keywords:
            if keyword.lower() in str(row):
                degree_list.append(degree)
    return degree_list


def match_quals(row):
    qual_list = []
    for qual in job_qualifications:
        if qual.lower() in str(row):
            qual_list.append(qual)
    return qual_list


def clean_up_dataframe(raw_disney_df):
    """ Disney dataframe is going through some stuff, clean up the columns and change types """
    # resetting the index
    raw_disney_df.reset_index(inplace=True)
    print(raw_disney_df.head())
    # and renaming unnamed job id column
    raw_disney_df.rename(columns= {"index" : "job_id"}, inplace=True)
    print(raw_disney_df.head())
    # convert to string (in case it's all nulls) and make lowercase
    raw_disney_df["responsibilities"] =  raw_disney_df["responsibilities"].astype(str).str.lower()
    raw_disney_df["basic_qualifications"] = raw_disney_df["basic_qualifications"].astype(str).str.lower()
    raw_disney_df["preferred_qualifications"] = raw_disney_df["preferred_qualifications"].astype(str).str.lower()
    raw_disney_df["education"] = raw_disney_df["education"].astype(str).str.lower()
    raw_disney_df["preferred_education"] = raw_disney_df["preferred_education"].astype(str).str.lower()
    raw_disney_df["key_qualifications"] = raw_disney_df["key_qualifications"].astype(str).str.lower()
    # combine it all cause disney has no consistency across posts
    raw_disney_df["all"] = raw_disney_df["basic_qualifications"] + raw_disney_df["preferred_qualifications"] + raw_disney_df["key_qualifications"] + raw_disney_df["education"] + raw_disney_df["preferred_education"]
    raw_disney_df.drop(columns = [
        "basic_qualifications", "preferred_qualifications", "key_qualifications", "education", "preferred_education"
        ], inplace=True)
    return raw_disney_df


def split_up_dataframe(raw_disney_df, start_date):
    """ Check for keywords and throw away the rest """
    clean_disney_df = clean_up_dataframe(raw_disney_df)
    # use functions to get degree mentions or qualification keywords
    clean_disney_df["education_keywords"] = clean_disney_df["all"].apply(match_education)
    clean_disney_df["qual_keywords"] = clean_disney_df["all"].apply(match_quals)
    # only grab necessary columns
    clean_disney_df = clean_disney_df[["job_id", "title", "locations", "posting_date", "education_keywords", "qual_keywords"]]
    """ Creates four different dataframes for: location, education, qualifications, and the raw tables """
    # rename index for future 
    clean_disney_df.index.name = "dim_id"
    # create separate tables
    dimension_table = clean_disney_df[["job_id", "title", "posting_date"]]
    locations_table = clean_disney_df.drop(columns=["job_id", "title", "posting_date", "education_keywords", "qual_keywords"])
    education_table = clean_disney_df.drop(columns=["job_id", "title", "posting_date", "locations", "qual_keywords"])
    qualifications_table = clean_disney_df.drop(columns=["job_id", "title", "posting_date", "locations", "education_keywords"])
    # rename dimension table id 
    dimension_table.rename(columns = {"dim_id": "id"}, inplace=True)
    # break our lists apart and give them back a real index
    education_table = education_table.explode("education_keywords").reset_index()
    qualifications_table = qualifications_table.explode("qual_keywords").reset_index() 
    locations_table = locations_table.where(pd.notnull(locations_table), None) # turn NaNs into Nones
    locations_table = locations_table.explode("locations").reset_index()
    # locations has trailing and leading spaces
    locations_table["locations"] = locations_table["locations"].str.strip()
    
    return [dimension_table, locations_table, education_table, qualifications_table]