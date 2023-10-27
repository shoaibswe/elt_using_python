import argparse
from pathlib import Path

from model import Connection
import dags.scripts.config as config


def init_csv_file():
    Path(config.CSV_FILE_DIR).mkdir(parents=True, exist_ok=True)

# Initialize schema and table
def init_db():
    # Stablish a db connection
    # get db session
    # create a schema named raw
    # create users, locations, additional table in schema raw with appropiate columns
    # commit db
    # close db
    pass


if __name__ == '__main__':
    init_csv_file()
    init_db()
