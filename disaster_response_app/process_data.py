import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    categories = pd.read_csv(categories_filepath)
    messages = pd.read_csv(messages_filepath)
    
    df = messages.merge(categories, on='id')
    return df


def clean_data(df):
    df_raw = df.drop_duplicates(subset='id')
    cats = df_raw.categories.str.split(';')[0]    
    cats_list = []
    for i in cats:
        i = i[:-2]
        cats_list.append(i)
        
    temp = df_raw.categories.str.split(';', expand=True)
    df = pd.concat([df_raw, temp], axis=1)
    
    df.columns = df.columns[:5].tolist() + cats_list
    df.drop('categories', axis=1 ,inplace=True)
    
    for i in df.columns[4:]:
        df[i] = df[i].str[-1:]
        
    return df

def save_data(df, database_filename):
    conn = sqlite3.connect(database_filename)
    conn.text_factory = str

    df.to_sql('disaster_messages', con = conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
#     engine = create_engine('sqlite:///'+database_filename)

#     conn = engine.connect()

#     df.to_sql('disaster_messages', engine, index=False, if_exists='replace')

#     conn.close()
#     engine.dispose()

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()