import os
import csv

from model import Connection, Users, Locations, Additional
import dags.scripts.config as config

def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    # write your code here
    filename = "random_user.csv"
    filepath = ''
    return filepath

def main():
    filename = get_file_path()
    data_insert = []

    # read the csv file
    # Create users, locations, additinal object
    # insert these object in the array and then into our data warehouse
    with open(filename, encoding='utf-8') as csvf:
        for row in csv_reader:
            pass
            #user = Users(name=row['name'])

    # Connect with the db
    # get a sessions
    # First delete all previous users table data from schema raw
    # load data into db
    # commit db
    # close db
    # write your code here

if __name__ == '__main__':
    main()
