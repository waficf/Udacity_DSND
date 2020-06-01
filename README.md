# DEND Capstone Project
------


# Scope of the project
---

The goal of this project is to demonstrate our abilities to execute a full ETL process from a databse and get it ready and automated

The purpose here is to use the weather and demogrpahics dataset provided by Udacity which I merged with the flights data provided in another Udacity Nanodegree to enable data analysts analyzing how flights are affected by these factors.

The amount of data in flights and weather changes a lot unlike that of demogrpahics. So I decided to run the ETL using Airflow weekly to update the needed tables


### Technology Used
----
- AWS Redshift: Amazing scalable data storage that handles spikes in queries without scarificing performance
- Apache Airflow: Allows easy execution of ETL DAGs amd handles huge amounts of data and processes by running parallel DAGs that are independent. For example, in the ETL we can stage 3 different table in parallel without any delays
- Python 3.6

### Python Scripts
---
- etl_dag.py: Takes the staging tables and load them into the final tables
- create_table_dag.py: Create both staging and final tables
- sql_queries.py: Queries the database to transfer the tables from S3 to Redshift but executes only via the Airflow process

# Explore and Assess Data

- Global weather data provided by Udacity
- US demographics data also provided by Udacity
- US flights data from BST available in this link: transtats.bts.gov

# Schema and Data Dictionary
---

I chose a simple schema, the flight and weather data refers to cities and since demographcs reference cities, then now we have a relationship between the 3 tables

#### Staging Tables
- staging_weather: Extracts the weather data as it is from source
- staging_us_demographics: Extracts the US demogrpahics as it is from source
- staging_us_flights: Extracts the US Flights as it is from source


## Data Dictionary 


#### Fact Table & Dimensional Table
Cities Table: It includes the data extracted from flights:
- city_id BIGINT 
- city_name VARCHAR
- state_name VARCHAR
- state_code VARCHAR

Flights Table: Has flight data extracted from flights:

- flight_id BIGINT
- flight_date DATE NOT NULL
- original_city_name VARCHAR
- destination_city_name VARCHAR

Demographics:
- city_id VARCHAR PRIMARY KEY,
- median_age DECIMAL,
- male_population BIGINT,
- female_population BIGINT,
- total_population BIGINT,
- number_veterans BIGINT,
- foreign_born BIGINT,
- avg_household_size DECIMAL,
- RACE VARCHAR,
- count BIGINT,

Weather:
- city VARCHAR PRIMARY KEY,
- avg_temp DECIMAL,
- avg_temp_uncertainty DECIMAL,
- city_id BIGINT,
- country VARCHAR,
- dates Date

Time Table:
- dates TIMESTAMP PRIMARY KEY, 
- day INT, 
- month INT, 
- year INT


# ETL Model
---

I used apache Airflow to take data from S3 to Redshift, stage them into 3 tables and then extract, load and transform them a data quality check then 

## Scenarios
---

- More than 1M lines of data: Redshift can handle data increase by 100X
- Pipeline can be adjusted easily to run daily at 7
- 100+ people accessing database: The more users accessing the database the more CPU resources we will need that is why AWS Redshift. As per AWS website, Redshift distibutes and parallelizate across multiple physical resources and as the number of users increase you will not experience delays in the query response because the use of Concurrency Scaling that handles spikes in workloads while maintaining consistent SLAs.


## Conclusion
---

The choice of technology in terms of using cloud storage in AWS or using advance ETL process in Airflow are all practices of data engineering technology

