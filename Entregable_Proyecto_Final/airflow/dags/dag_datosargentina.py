from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email_operator import EmailOperator

from scripts.main import load_exportaciones_data

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=1)
}

with DAG(
    dag_id="dag_datosargentina",
    start_date=datetime(2020, 1, 1),
    catchup=False,
    schedule_interval='@monthly',
    default_args=default_args
) as dag:

    # task con dummy operator
    dummy_start_task = DummyOperator(
        task_id="start"
    )

    create_tables_task = PostgresOperator(
        task_id="create_tables",
        postgres_conn_id="coderhouse_redshift",
        sql="sql/creates.sql",
        hook_params={	
            "options": "-c search_path=mancinijulian8_coderhouse"
        }
    )

    load_exportaciones_data_task = PythonOperator(
        task_id="load_exportaciones_data",
        python_callable=load_exportaciones_data,
        op_kwargs={
            "config_file": "/airflow/config/config.ini"
        }
    )

    email_notification_task = EmailOperator(
    task_id="send_email_notification",
    to="mancinijulian8@gmail.com",
    subject="Notificación de éxito del DAG datosargentina",
    html_content="<p>El proceso fue exitoso.</p>",
    mime_charset="utf-8"
)

    dummy_end_task = DummyOperator(
        task_id="end"
    )

    dummy_start_task >> create_tables_task
    create_tables_task >> load_exportaciones_data_task
    load_exportaciones_data_task >> dummy_end_task
    dummy_end_task >> email_notification_task