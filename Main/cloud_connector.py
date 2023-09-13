import psycopg2
import pandas as pd


def read_csv(filename):
    # Read csv file and package it into a pandas dataframe
    # return the dataframe
    return


def get_data(dataframe):
    # Trim the dataframe, until we are left with the relevant columns:
    # Datetime, sensor_id/unit no., temperature, acceleration XYZ
    # return trimmed dataframe
    return


def write_data(dataframe):
    # SQL instruction to query latest data's datetime
    # If data's datetime not same with dataframe's datetime
    # Then we write data into correct location, return True
    # Else, we return False
    return


connection = psycopg2.connect(user="dbfirenet_user", password="G9Fw38n8WjMfN4zTBydkxYqZFefZSiM4", host="dpg-ck0lntu3ktkc73f98tcg-a.singapore-postgres.render.com", port="5432", database="dbfirenet")
cursor = connection.cursor()


while True:
    
    df = get_data(read_csv('data_manager.csv'))
    
    if write_data(df):
        print('New data recorded!')
    else:
        print('Waiting for new data...')
