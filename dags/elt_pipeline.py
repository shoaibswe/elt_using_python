import os
# import sys 
# sys.path.insert(0,'/opt/airflow/dags/scripts')

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
    description='An ETL dag for random user data loads to warehouse',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 10, 27),
    catchup=False) as dag:

    migration = BashOperator(
    task_id = 'migration',
    bash_command = 'python /opt/airflow/dags/scripts/migration.py'    
    )

extract = BashOperator (
    task_id ='extract',
    bash_command ='python /opt/airflow/dags/scripts/extract.py'
)

load = BashOperator(
    task_id = 'load',
    bash_command = 'python /opt/airflow/dags/scripts/load.py'
    )

migration >> extract >> load 

    # pass