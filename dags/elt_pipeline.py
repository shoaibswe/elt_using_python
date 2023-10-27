import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
'owner': 'airflow',
'depends_on_past': False,
'email_on_failure':False,
'email_on_retry':False,
'retries':3,
'retry_delay': timedelta(minutes=3)
}

with DAG(
    'ELT',
    # write you extract and load airflow dag here
    # the dag should have four bash operators
    # migration >> extract >> load
    default_args=default_args,
    description='An ETL dag for random user data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 10, 26),
    catchup=False) as dag:

    migration = BashOperator(
    task_id = 'migration',
    bash_command = 'python scripts/migration.py'    
    )

extract = BashOperator (
    task_id ='extract',
    bash_command ='python scripts/extract.py'
)

load = BashOperator(
    task_id = 'load',
    bash_command = 'python scripts/load.py'
    )

migration >> extract >> load 

    # pass