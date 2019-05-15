# Starbucks Customer Segmentation

I wanted to segment starbucks customers based on their demographics and spending behavior provided through the offers data available from Udacity.

The data contains 3 sets of 'porfolio', 'profile' and 'transcripts'. It represents 17,000 
customers on the Starbucks rewards mobile app where starbucks sends an offer every few days. 

The goal is to use this data to build up a a more comprehensive customer profile that will allow us to segment these customers.

The task was not easy because I chose this dataset based on my interest in the topic and the company rather what is available on the table, the data required lots of preprocessing and feature engineering which ate most of the time invested leaving little time to analyze and try to pick up trends before the project deadline

I created and played around the data and reached that the customers can be broken down to 8 clusters using k-means clustering.

## Install
This project requires Python 3.x and the following Python libraries installed:

import pandas as pd
import numpy as np
import math
import json
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import seaborn as sns

## The data is contained in three files:

portfolio.json - containing offer ids and meta data about each offer (duration, type, etc.)
profile.json - demographic data for each customer
transcript.json - records for transactions, offers received, offers viewed, and offers completed
Here is the schema and explanation of each variable in the files:

#### portfolio.json

id (string) - offer id
offer_type (string) - type of offer ie BOGO, discount, informational
difficulty (int) - minimum required spend to complete an offer
reward (int) - reward given for completing an offer
duration (int) - time for offer to be open, in days
channels (list of strings)

#### profile.json

age (int) - age of the customer
became_member_on (int) - date when customer created an app account
gender (str) - gender of the customer (note some entries contain 'O' for other rather than M or F)
id (str) - customer id
income (float) - customer's income

#### transcript.json

event (str) - record description (ie transaction, offer received, offer viewed, etc.)
person (str) - customer id
time (int) - time in hours since start of test. The data begins at time t=0
value - (dict of strings) - either an offer id or transaction amount depending on the record


## Project Introduction
Not all users receive the same offer, and it is unlcear which offers get to be linked to which transactions and then there is the offer validity date and more confusing are which customers completeed the offer because they found it interesting and those who completed it without knowledge of the offer whatsoever.

The data also included lots of missing points in terms of income and gender with 118 years old for some customers where I used machine learning algorithms to fill these values


