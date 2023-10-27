import os
import csv

from scripts.model import Connection, Users, Locations, Additional
# import dags.scripts.config as config
# import sys
# sys.path.insert(0,'/Users/shuvo/Documents/doc/Take-Home-Assignment-main/dags/')
# import scripts.config as config
from scripts.config import DB_CONNECTION_STRING_WAREHOUSE 

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    # write your code here
    filename = "random_user.csv"
    filepath = os.path.join(os.getcwd(), filename)
    return filepath

def main():
    filename = get_file_path()
    data_insert = []

    # read the csv file
    # Create users, locations, additinal object
    # insert these object in the array and then into our data warehouse
    with open(filename, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        header_row = csv_reader.fieldnames
        print(header_row)

        # for row in csv_reader:
        #     user = Users(name=row['name'])
        #     location = Locations(city=row['location_city'], state=row['location_state'])
        #     additional = Additional(email=row['email'], phone=row['phone'])
        #     user.location = location
        #     user.additional = additional
        #     data_insert.append(user)

            # pass
            #user = Users(name=row['name'])

    # Connect with the db
    # get a sessions
    # First delete all previous users table data from schema raw
    # load data into db
    # commit db
    # close db
    # write your code here
    engine = create_engine(DB_CONNECTION_STRING_WAREHOUSE)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.query(Users).delete()
        session.bulk_save_objects(data_insert)
        session.commit()
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    main()
