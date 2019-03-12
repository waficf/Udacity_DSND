# Disaster Response Web App

## Installation
The code requires the following Python packages: json, plotly, pandas, nltk, flask, sklearn, sqlalchemy, sys, numpy, re, pickle and written in python 3.6

## Project Overview
This app classifies messages recieved from people in the occurance of a disaster to be directed to the right aid agency


## File Descriptions
process_data.py: This code takes as its input csv files containing message data and message categories (labels), and creates a clean SQLite database
train_classifier.py: This code takes the SQLite database produced by process_data.py as an input and uses the data contained within it to train and tune a ML model for categorizing messages. 
ETL Pipeline Preparation.ipynb: This is the playground on which process.py was created 
ML Pipeline Preparation.ipynb: This is the playground on which train_classifier.py was created

## Running Instructions
Run process_data.py
Save the data folder in the current working directory and process_data.py in the data folder.
Run the following command in the shell: python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
Run train_classifier.py in shell 
In the current working directory, create a folder called 'models' and save train_classifier.py in this.

Run the following command in the shell: python run.py
