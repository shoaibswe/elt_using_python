import os

API_URL = os.getenv("API_URL", "https://randomuser.me/api/?seed={}")
CSV_FILE_DIR = os.getenv("CSV_FILE_DIR", "/opt/airflow/dags/datasets/")
SEED = 'ABCDEFGHI'

POSTGRES_DB = os.getenv("POSTGRES_DB", "warehouse")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "warehouse")
DB_CONNECTION_STRING_WAREHOUSE = os.getenv("DB_CONNECTION_STRING", "postgresql+psycopg2://admin:admin@warehouse/warehouse")
