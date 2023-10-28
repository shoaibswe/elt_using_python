import csv
import sys
sys.path.insert(0,'/opt/airflow/dags/scripts')
# sys.path.insert(0,'/Users/shuvo/Documents/doc/Take-Home-Assignment-main/dags/scripts')
import uuid

from model import Connection, Users, Locations, Additional
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
    # filename ='/Users/shuvo/Documents/doc/Take-Home-Assignment-main/dags/scripts/random_user.csv'
    print("Debug file path is: ",filename)
    return filename
    
def main():
    filename = get_file_path()
    data_insert_users = []
    data_insert_locations = []
    data_insert_additional = []

    engine = create_engine(DB_CONNECTION_STRING_WAREHOUSE)
    Session = sessionmaker(bind=engine)
    session = Session()
    # read the csv file
    # Create users, locations, additinal object
    # insert these object in the array and then into our data warehouse
    with open(filename, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        print("Debug csv reader", csv_reader)
        for row in csv_reader:
            user_data = {
                'Gender': row.get('Gender', None),
                'Name': {
                    'Name': row.get('Name', None),
                },
                'First Name': {
                    'First': row.get('First Name', None),
                },
                'Last Name': {
                    'Last': row.get('Last Name', None),
                },
                'Date of Birth': row.get('Date of Birth', None),
                'City': row.get('City', None),
                'State': row.get('State', None),
                'Country': row.get('Country', None),
                'Postcode': row.get('Postcode', None),
                'Country Code (nat)': row.get('Country Code (nat)', None),
                'Phone': row.get('Phone', None),
                'Email': row.get('Email', None),
                'Picture Large': row.get('Picture Large', None)
            }
            
            user_id = uuid.uuid4()
            user = Users(
                id=user_id,
                gender=user_data.get('Gender', None),
                name=user_data.get('Name', {}).get('Name', None),
                first=user_data.get('First Name', {}).get('First', None),
                last=user_data.get('Last Name', {}).get('Last', None),
                date_of_birth=user_data.get('Date of Birth', None)
            )
            data_insert_users.append(user)

            location_data = {
                'city': user_data.get('City', None),
                'state': user_data.get('State', None),
                'country': user_data.get('Country', None),
                'postcode': user_data.get('Postcode', None),
                'country_code': user_data.get('Country Code (nat)', None),
                'user_id': user_id
            }
            location_id = uuid.uuid4()
            location = Locations(id=location_id, **location_data)
            location.user = user
            data_insert_locations.append(location)

            additional_data = {
                'id': uuid.uuid4(),
                'phone': user_data.get('Phone', None),
                'email': user_data.get('Email', None),
                'picture_large': user_data.get('Picture Large', None),
                'user_id': user_id
            }
            additional = Additional(**additional_data)
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

        for location in data_insert_locations:
            location.user_id = location.user.id

        for additional in data_insert_additional:
            additional.user_id = additional.user.id

        session.bulk_save_objects(data_insert_locations)
        session.bulk_save_objects(data_insert_additional)
        session.commit()
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    main()
