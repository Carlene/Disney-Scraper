# Disney Data Job Scraper

This scraper can be given a Disney job search link (at the moment, it pulls all Data Engineering related jobs), and it will pull information about each job's:
* Title
* Path to Job Posting
* Posting Date
* Location
* Brand
* Responsibilities
* Education
* Qualifications

It will then create a CSV that saves both locally and to the given S3 bucket, then pull data from the bucket into the given redshift database and table. 