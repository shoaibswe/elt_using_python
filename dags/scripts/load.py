import os
import csv
import sys
sys.path.insert(0,'/opt/airflow/dags/scripts')
import json

from model import Connection, Users, Locations, Additional
# import sys
# sys.path.insert(0,'/Users/shuvo/Documents/doc/Take-Home-Assignment-main/dags/')
from config import DB_CONNECTION_STRING_WAREHOUSE 

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_file_path():
    # should return a os file path with correct destination.
    # Do not change file name
    # write your code here
    # filename = "random_user.csv"
    # filepath = os.path.join(os.getcwd(), filename)
    # return filepath
    filename ='/opt/airflow/dags/scripts/random_user.csv'
    return filename

def preprocess_json(json_str):
    last_closing_brace = json_str.rfind('}')
    if last_closing_brace != -1:
        json_str = json_str[:last_closing_brace + 1]
    json_str = json_str.replace("{}/[0],1,1,1.4", "")
    return json_str

def extract_data_from_json(json_str):
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}. Returning an empty dictionary.")
        return {}
    
def main():
    filename = get_file_path()
    data_insert_users = []
    data_insert_locations = []
    data_insert_additional = []
    user_id_mapping = {}

    engine = create_engine(DB_CONNECTION_STRING_WAREHOUSE)
    Session = sessionmaker(bind=engine)
    session = Session()
    # read the csv file
    # Create users, locations, additinal object
    # insert these object in the array and then into our data warehouse
    with open(filename, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)

        for row in csv_reader:
            # results_json = preprocess_json(row.get('results', '{}'))
            # info_seed_json = preprocess_json(row.get('info_seed', '{}'))
            # info_results_json = preprocess_json(row.get('info_results', '{}'))
            results_json = preprocess_json(row.get('results', '{}'))
            user_data = extract_data_from_json(results_json)

            print("Results JSON:", results_json)
            # print("Info Seed JSON:", info_seed_json)
            # print("Info Results JSON:", info_results_json)

            # user_data = extract_data_from_json(results_json)
            # location_data = extract_data_from_json(info_seed_json)
            # additional_data = extract_data_from_json(info_results_json)
            user = Users(
                gender=user_data.get('gender', None),
                name=user_data.get('name', {}).get('title', None),
                first=user_data.get('name', {}).get('first', None),
                last=user_data.get('name', {}).get('last', None),
                date_of_birth=user_data.get('dob', {}).get('date', None)             
                )
            data_insert_users.append(user)
            # user = Users(
            #     gender=user_data.get('gender', None),
            #     name=user_data.get('name', {}).get('title', None),
            #     first=user_data.get('name', {}).get('first', None),
            #     last=user_data.get('name', {}).get('last', None),
            #     date_of_birth=user_data.get('dob', {}).get('date', None)
            # )
            # data_insert_users.append(user)

            location_data = user_data.get('location', {})
            location = Locations(
                city=location_data.get('city', None),
                state=location_data.get('state', None),
                country=location_data.get('country', None),
                postcode=location_data.get('postcode', None),
                country_code=location_data.get('country_code', None)
                )
            location.user = user
            data_insert_locations.append(location)

            additional_data = {
                'phone': user_data.get('phone', None),
                'email': user_data.get('email', None),
                'picture_large': user_data.get('picture', {}).get('large', None)
            }
            additional = Additional(
                phone=additional_data.get('phone', None),
                email=additional_data.get('email', None),
                picture_large=additional_data.get('picture_large', None)
            )
            additional.user = user
            data_insert_additional.append(additional)


    # Connect with the db
    # get a sessions
    # First delete all previous users table data from schema raw
    # load data into db
    # commit db
    # close db
    # write your code here

    try:
        session.bulk_save_objects(data_insert_users)
        session.commit()
        user_id_mapping = {user.id: user for user in data_insert_users}
        for location in data_insert_locations:
            location.user_id = location.user.id

        for additional in data_insert_additional:
            additional.user_id = additional.user.id
        session.bulk_save_objects(data_insert_locations)
        session.bulk_save_objects(data_insert_additional)

        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    main()
