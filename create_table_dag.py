from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
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

dag = DAG('create_tables_dag',
          default_args=default_args,
          description='Drop Create tables in Airflow'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)



DROP_STAGING_WEATHER_DAG = PostgresOperator(
    task_id = "drop_staging_weather",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_STAGING_WEATHER
    )


DROP_STAGING_US_DEMOGRAPHICS_DAG = PostgresOperator(
    task_id = "drop_staging_us_demographics",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_STAGING_US_DEMOGRAPHICS
    )



DROP_STAGING_FLIGHTS_DAG = PostgresOperator(
    task_id = "drop_staging_flights",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_STAGING_FLIGHTS
    )


DROP_DEMOGRAPHICS_DAG = PostgresOperator(
    task_id = "drop_demographics",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_DEMOGRAPHICS
    )


DROP_FLIGHTS_DAG = PostgresOperator(
    task_id = "drop_flights",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_FLIGHTS
    )


DROP_WEATHER_DAG = PostgresOperator(
    task_id = "drop_weather",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_WEATHER
    )


DROP_TIME_DAG = PostgresOperator(
    task_id = "drop_time",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_TIME
    )


DROP_CITIES_DAG = PostgresOperator(
    task_id = "drop_cities",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.DROP_CITIES
    )

CREATE_STAGING_WEATHER_DAG = PostgresOperator(
    task_id = "create_staging_weather",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_STAGING_WEATHER
    )


CREATE_STAGING_US_DEMOGRAPHICS_DAG = PostgresOperator(
    task_id = "create_staging_us_demographics",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_STAGING_US_DEMOGRAPHICS
    )


CREATE_STAGING_FLIGHTS_DAG = PostgresOperator(
    task_id = "create_staging_flights",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_STAGING_FLIGHTS
    )


CREATE_CITIES_DAG = PostgresOperator(
    task_id = "create_cities",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_CITIES
    )


CREATE_FLIGHTS_DAG = PostgresOperator(
    task_id = "create_flights",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_FLIGHTS
    )


CREATE_DEMOGRAPHICS_DAG = PostgresOperator(
    task_id = "create_demographics",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_DEMOGRAPHICS
    )


CREATE_WEATHER_DAG = PostgresOperator(
    task_id = "create_weather",
    dag=dag,
    postgres_conn_id = "redshift",
    sql = sql_queries.CREATE_WEATHER
    )


CREATE_TIME_TABLE_DAG = PostgresOperator(
    task_id = "create_time_table",
    dag=dag,
    postgres_conn_id = "redshift",
CREATE_TIME_TABLE = PostgresOperator(
    sql = sql_queries.CREATE_TIME_TABLE
    )


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)



start_operator >> DROP_STAGING_WEATHER_DAG
start_operator >> DROP_STAGING_US_DEMOGRAPHICS_DAG 
start_operator >> DROP_STAGING_FLIGHTS_DAG
start_operator >> DROP_DEMOGRAPHICS_DAG
start_operator >> DROP_FLIGHTS_DAG
start_operator >> DROP_WEATHER_DAG
start_operator >> DROP_CITIES_DAG
start_operator >> DROP_TIME_DAG

DROP_STAGING_WEATHER_DAG >> CREATE_STAGING_WEATHER_DAG
DROP_STAGING_US_DEMOGRAPHICS_DAG >> CREATE_STAGING_US_DEMOGRAPHICS_DAG
DROP_STAGING_FLIGHTS_DAG >> CREATE_STAGING_FLIGHTS_DAG
DROP_CITIES_DAG >> CREATE_CITIES_DAG
DROP_FLIGHTS_DAG >> CREATE_FLIGHTS_DAG
DROP_DEMOGRAPHICS_DAG >> CREATE_DEMOGRAPHICS_DAG
DROP_WEATHER_DAG >> CREATE_WEATHER_DAG
DROP_TIME_DAG >> CREATE_TIME_TABLE_DAG

CREATE_STAGING_WEATHER_DAG >> end_operator
CREATE_STAGING_US_DEMOGRAPHICS_DAG >> end_operator
CREATE_STAGING_FLIGHTS_DAG >> end_operator
CREATE_CITIES_DAG >> end_operator
CREATE_FLIGHTS_DAG >> end_operator
CREATE_DEMOGRAPHICS_DAG >> end_operator
CREATE_WEATHER_DAG >> end_operator
CREATE_TIME_TABLE_DAG >> end_operator





