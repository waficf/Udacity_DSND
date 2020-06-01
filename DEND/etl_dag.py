from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import sql_queries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past' : False,
    'retries' : 3,
    'catchup' : False,
    'email_on_retry' : False,
    'retry_delay' : timedelta(minutes = 5)
}

dag = DAG('etl_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@weekly'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


stage_weather_to_redshift = StageToRedshiftOperator(
    task_id='Stage_weather',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_weather",
    s3_path = "s3://wfahme/weather_data.csv" #Add weather from Kaggle
)


stage_demographics_to_redshift = StageToRedshiftOperator(
    task_id='Stage_demographics',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_us_demographics",
    s3_path = "s3://wfahme/us-demographics.csv" #Add US demographics
)


stage_flight_to_redshift = StageToRedshiftOperator(
    task_id='Stage_flights',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_us_flights",
    s3_path = "s3://wfahme/flights_US.csv" # Add flights data
)



# Loading starts here 

load_cities_from_staging_flights = LoadDimensionOperator(
    task_id='load_cities',
    dag=dag,
    redshift_conn_id="redshift",
    table="cities",
    insert_sql_query=sql_queries.LOAD_CITIES_TABLE,
    delete_before_insert=True
)


load_demographics_table = LoadFactOperator(
    task_id='load_demographics',
    dag=dag,
    redshift_conn_id="redshift",
    table="demographics",
    insert_sql_query=sql_queries.LOAD_DEMOGRAPHICS_TABLE,
    delete_before_insert=True
)


load_time_table = LoadDimensionOperator(
    task_id='load_time',
    dag=dag,
    redshift_conn_id="redshift",
    table="time_table",
    insert_sql_query=sql_queries.LOAD_TIME_TABLE,
    delete_before_insert=True
)


load_flight_table = LoadFactOperator(
    task_id='load_flights',
    dag=dag,
    redshift_conn_id="redshift",
    table="flights",
    insert_sql_query=sql_queries.LOAD_FLIGHTS_TABLE,
    delete_before_insert=True
)


load_weather_table = LoadFactOperator(
    task_id='load_weather',
    dag=dag,
    redshift_conn_id="redshift",
    table="weather",
    insert_sql_query=sql_queries.LOAD_WEATHER_TABLE,
    delete_before_insert=True
)

 
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables = ["flights", "time_table", "weather", "demographics", "cities"]

)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> stage_weather_to_redshift
start_operator >> stage_demographics_to_redshift
start_operator >> stage_flight_to_redshift


stage_flight_to_redshift >> load_cities_from_staging_flights
stage_flight_to_redshift >> load_time_table
stage_flight_to_redshift >> load_flight_table
stage_weather_to_redshift >> load_cities_from_staging_flights >> load_weather_table
stage_demographics_to_redshift >> load_cities_from_staging_flights >> load_demographics_table

load_cities_from_staging_flights >> run_quality_checks
load_time_table >> run_quality_checks
load_flight_table >> run_quality_checks
load_weather_table >> run_quality_checks
load_demographics_table >> run_quality_checks

run_quality_checks >> end_operator






