import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta



with DAG(
    'ELT',
) as dag:
    # write you extract and load airflow dag here
    # the dag should have four bash operators
    # migration >> extract >> load
    pass
