# Drop Tables for staging to run DAG
DROP_STAGING_WEATHER = """DROP TABLE IF EXIST public.staging_weather"""
DROP_STAGING_US_DEMOGRAPHICS = """DROP TABLE IF EXIST public.staging_us_demographics"""
DROP_STAGING_FLIGHTS = """DROP TABLE IF EXISTS public.staging_us_flights"""

DROP_DEMOGRAPHICS = """DROP TABLE IF EXIST public.demographics"""
DROP_FLIGHTS = """DROP TABLE IF EXIST public.flights"""
DROP_WEATHER = """DROP TABLE IF EXIST public.weather"""

DROP_TIME = """DROP TABLE IF EXIST public.time_table"""
DROP_CITIES = """DROP TABLE IF EXIST public.cities"""

# Create Staging Tables 

## Weather as per the Kaggle link
CREATE_STAGING_WEATHER = """
	CREATE TABLE public.staging_weather(
	dt DATE,
	avg_temp DECIMAL,
	avg_temp_uncertainty DECIMAL,
	city VARCHAR,
	country VARCHAR,
	latitude VARCHAR,
	longitute VARCHAR
	);

"""

## US Demographics as per public.opendatasoft.com
CREATE_STAGING_US_DEMOGRAPHICS = """
	CREATE TABLE public.staging_us_demographics(
	city VARCHAR,
	state VARCHAR,
	RACE VARCHAR,
	count BIGINT,
	median_age DECIMAL,
	male_population BIGINT,
	female_population BIGINT,
	total_population BIGINT,
	number_veterans BIGINT,
	foreign_born BIGINT,
	avg_household_size DECIMAL,
	state_code VARCHAR
	);

"""

## US Flights 
CREATE_STAGING_FLIGHTS = """
	CREATE TABLE public.staging_us_flights(
	year INTEGER,
	month INTEGER,
	flight_date TIMESTAMP,
	reporting_airline VARCHAR,
	original_city_name VARCHAR,
	original_state_code VARCHAR,
	original_state_name VARCHAR,
	destination_city_name VARCHAR,
	destination_state_code VARCHAR,
	destination_state_name VARCHAR,
	);
"""


# Create Fact and dimensional Tables

CREATE_CITIES = """
	CREATE TABLE public.cities(
	city_id BIGINT IDENTITY(0,1) PRIMARY KEY,
	city_name VARCHAR,
	state_name VARCHAR,
	state_code VARCHAR
	);
"""

CREATE_FLIGHTS = """
	CREATE TABLE public.flights(
	flight_id BIGINT IDENTITY(0,1) PRIMARY KEY,
	flight_date DATE NOT NULL,
	original_city_name VARCHAR,
	destination_city_name VARCHAR
	);
"""


CREATE_DEMOGRAPHICS = """
	CREATE TABLE public.demographics(
	city_id VARCHAR PRIMARY KEY,
	median_age DECIMAL,
	male_population BIGINT,
	female_population BIGINT,
	total_population BIGINT,
	number_veterans BIGINT,
	foreign_born BIGINT,
	avg_household_size DECIMAL,
	RACE VARCHAR,
	count BIGINT,
	);
"""

CREATE_WEATHER = """
	CREATE TABLE public.weather(
	city VARCHAR PRIMARY KEY,
	avg_temp DECIMAL,
	avg_temp_uncertainty DECIMAL,
	city_id BIGINT,
	country VARCHAR,
	dates Date
	);
"""

CREATE_TIME_TABLE = """
	CREATE TABLE public.time_table(
    dates TIMESTAMP PRIMARY KEY, 
    day INT, 
    month INT, 
    year INT
	);
"""

# SQL Load Facts and dimensional Tables for DAG
LOAD_CITIES_TABLE = """
	SELECT 	city_name, state_name, state_code 
	FROM (SELECT SPLIT_PART(UPPER((original_city_name),', ',1) AS city_name,
					UPPER(original_state_name) AS state_name,
					original_state_code AS state_code
					FROM staging_us_flights)
"""



LOAD_DEMOGRAPHICS_TABLE = """
	SELECT 
	c.city_id,
	st_dem.median_age,
	st_dem.male_population,
	st_dem.female_population,
	st_dem.total_population,
	st_dem.number_veterans,
	st_dem.foreign_born,
	st_dem.avg_household_size,
	st_dem.RACE,
	st_dem.count

	FROM staging_us_demographics AS st_dem
	JOIN CITIES AS c

	ON UPPER(st_dem.city) = c.city_name

"""

LOAD_TIME_TABLE = """
	SELECT 
    flight_date, 
    extract(DAY from flight_date) as day, 
    month, 
    year

    FROM staging_us_flights

"""

LOAD_FLIGHTS_TABLE = """
	SELECT 
	flight_date,
	original_city_name,
	destination_city_name

	FROM staging_us_flights

"""

LOAD_WEATHER_TABLE = """
	SELECT 
	sw.city,
	sw.avg_temp,
	sw.avg_temp_uncertainty,
	c.city_id,
	sw.country,
	sw.dt

	FROM staging_weather as sw 
	JOIN CITIES as c ON UPPER(sw.city) = c.city_name

"""










	
