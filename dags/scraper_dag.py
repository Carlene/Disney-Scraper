####################### Standard Libraries #####################################
import pytz
tz = pytz.timezone("US/Pacific")
from datetime import timedelta
from airflow import DAG, utils
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
####################### My Libraries ###########################################
from disney.run import main

default_args = {
    "start_date": utils.dates.days_ago(7),
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(seconds = 20),
    "schedule_interval": "0 12 * * *",
    "dagrun_timeout": timedelta(minutes = 40)
    }

with DAG(
    "disney_scraper",
    tags = ["scraper", "disney"],
    default_args = default_args,
    description = "Creates a csv in AWS with Disney job data",
    catchup = False 
    ) as disney_scraper_dag:

    disney_scraper_daily = PythonOperator(
        task_id = "disney_scraper", # The name of the table where it will post to.
        python_callable = main, # The main function.
        dag = disney_scraper_dag # The physical DAG that will execute.
        )