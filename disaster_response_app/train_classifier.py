import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import nltk
import re
from nltk.tokenize import word_tokenize
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.pipeline import Pipeline
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import pickle


def load_data(database_filepath):
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('disaster_messages', engine)
    X = df['message']
    Y = df.loc[:,'related':'direct_report']
    
    target_names = list(Y.columns)
    
    return X, Y, target_names


def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]",' ', text)
    
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    clean_token = []
    for token in tokens:
        text_token = lemmatizer.lemmatize(token).lower().strip()
        clean_token.append(text_token)
    
    return clean_token


def build_model():
    pipeline = Pipeline([('tfidf', TfidfVectorizer(tokenizer=tokenize)),
                         ('clf', MultiOutputClassifier(RandomForestClassifier()))])
    
    parameters = {
#     'tfidf__use_idf': (True, False),
#     'tfidf__stop_words':(None, 'english'),
#     'tfidf__ngram_range': ((1, 1),(1,3)),
    'clf__estimator__n_estimators': (15, 20),
#     'clf__estimator__min_samples_split': (2, 4),
#     'clf__estimator__max_features': ('auto', .5)
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    cv.fit(X_train, Y_train)
    
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = cv.predict(X_test)
    target_names = list(Y_test.columns)
    y_pred_df = pd.DataFrame(y_pred, columns=target_names)
    
    for i in y_pred_df.columns:
        print(i, '\n',classification_report(Y_test[i], y_pred_df[i]))
    
    


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()