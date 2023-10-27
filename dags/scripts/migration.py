import sys
sys.path.insert(0,'/opt/airflow/dags/scripts/')
# sys.path.insert(0,'/opt/airflow/scripts/')

import argparse
from pathlib import Path

from model import Connection
# from model import Connection
# import dags.scripts.config as config
# import sys
# sys.path.insert(0,'/Users/shuvo/Documents/doc/Take-Home-Assignment-main/dags/')
import config as config

from sqlalchemy import create_engine,text
import os

def init_csv_file():
    Path(config.CSV_FILE_DIR).mkdir(parents=True, exist_ok=True)

# Initialize schema and table
def init_db():
    # Stablish a db connection
    engine= create_engine(config.DB_CONNECTION_STRING_WAREHOUSE)
    # get db session
    
    
    # create a schema named raw
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # schema_file_path = os.path.abspath(os.path.join(script_dir,'..','..','scripts','schema.sql'))
    # table_file_path = os.path.abspath(os.path.join(script_dir,'..','..','scripts','table.sql'))
    schema_file_path = '/opt/airflow/scripts/schema.sql'
    table_file_path = '/opt/airflow/scripts/table.sql'
    # print("Script Dir is: ",script_dir)
    # print(schema_file_path)
    # print(table_file_path)
    connection = Connection(engine)
    session = connection.get_session()

    with open(schema_file_path, 'r') as schema_file:
        schema_commands = text(schema_file.read())
        try:
            session.execute(schema_commands)
            session.commit()
        except Exception as e:
            print(f"Error executing schema SQL: {e}")
            session.rollback()

    with open(table_file_path, 'r') as table_file:
        tbl_commands = text(table_file.read())
        try:
            session.execute(tbl_commands)
            session.commit()
        except Exception as e:
            print(f"Error executing table SQL: {e}")
            session.rollback()
    
    # create users, locations, additional table in schema raw with appropiate columns
    # commit db
    # close db

    session.commit()
    session.close()
    # pass


if __name__ == '__main__':
    init_csv_file()
    init_db()

#INSTALLED SQLALCHEMY