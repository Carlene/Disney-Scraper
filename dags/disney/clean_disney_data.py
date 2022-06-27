############################  FILTER DATAFRAME AT END #############################

job_qualifications = [
    'Python', 'R ', 'AWS', ' Warehouse', 'Data Warehouse', 'Hive', 'Azure', 'Cloud', 'Java', 'C++', 'C ', 
    'Airflow', 'SQL', 'Database', 'Postgres', 'Machine Learning', 'Big Data', 'ETL', 'Kafka', 'Spark', 'Scala',
    'Terraform', 'Redshift', 'Pipeline', 'Hadoop', 'Docker', 'GitLab', 'GitHub', 'Kubernetes', 'HCI', 'Linux', 
    'OSX', 'svn', 'Gradle', 'Maven', 'Swift', 'Matlab', 'MongoDB', 'Objective-C', 'Ruby', 'Perl', 'Pig', 'Hadoop',
    'Cosmos', 'Javascript']

education = {
    "bachelor's degree": ["B.S", "BS", "bachelor"],
    "associate's degree": ["associate's", "associates"],
    "master's degree": ["master's", "masters", "M.S", "MS"],
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


def clean_up_dataframe(disney_df):
    """ Disney dataframe is going through some stuff, clean up the columns and change types """
    # fixing unnamed id column
    disney_df.rename(columns= {"Unnamed: 0" : "id"}, inplace=True)
    # convert to string (in case its all nulls) and make lowercase
    disney_df["responsibilities"] =  disney_df["responsibilities"].astype(str).str.lower()
    disney_df["basic_qualifications"] = disney_df["basic_qualifications"].astype(str).str.lower()
    disney_df["preferred_qualifications"] = disney_df["preferred_qualifications"].astype(str).str.lower()
    disney_df["education"] = disney_df["education"].astype(str).str.lower()
    disney_df["preferred_education"] = disney_df["preferred_education"].astype(str).str.lower()
    disney_df["key_qualifications"] = disney_df["key_qualifications"].astype(str).str.lower()
    # locations has trailing and leading spaces
    disney_df["locations"] = disney_df["locations"].str.strip()
    # combine all qualification columns
    disney_df["all_qualifications"] = disney_df["basic_qualifications"] + disney_df["preferred_qualifications"] + disney_df["key_qualifications"]
    # combine all education columns
    disney_df["all_education"] = disney_df["education"] + disney_df["preferred_education"]
    disney_df.drop(columns = [
        "basic_qualifications", "preferred_qualifications", "key_qualifications", "education", "preferred_education"
        ], inplace=True)
    return disney_df


def find_keywords(disney_df):
    """ Check for keywords and throw away the rest """
    disney_df = clean_up_dataframe(disney_df)
    # use functions to get degree mentions or qualification keywords
    disney_df["education_keywords"] = disney_df["all_education"].apply(match_education)
    disney_df["qual_keywords"] = disney_df["all_qualifications"].apply(match_quals)
    # only grab necessary columns
    disney_df = disney_df[["id", "title", "locations", "posting_date", "education_keywords", "qual_keywords"]]
    return disney_df