import os
import pandas as pd
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import airflow
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.filesystem import FileSensor

# Parámetros de DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
    'schedule_interval': '@daily'
}

# Función que lee el archivo CSV
def read_csv_file():
    df = pd.read_csv("https://drive.google.com/u/0/uc?id=1IAb_x49xqjM-8cx-cpHkM1bnR6j-I4T6&export=download")
    return df

# Función que transforma los datos
def transform_data():
    df = read_csv_file()
    df = df.groupby(['STNAME', 'YEAR'])['AAWDT'].sum().reset_index().sort_values(by='AAWDT', ascending=False)
    df = df.reset_index()
    return df

# Función que exporta los datos transformados a un archivo CSV
def export_csv_data():
    df = transform_data()
    
    # Fecha y hora actual
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    
    # Nombrado de outfile
    output_filename = f"total_accidentes_por_calle_año_{timestamp}.csv"

    # Generar un nuevo archivo CSV
    df.to_csv(output_filename, index=False)

def export_db_data():
    df = transform_data()
    
    # Escribir el resultado en una tabla en una base de datos de PostgreSQL
    engine = create_engine('postgresql://airflow:airflow@localhost:5432/airflow')
    conn = engine.connect()
    conn.execute('CREATE TABLE IF NOT EXISTS accidentes_seattle (STNAME VARCHAR(255), YEAR INTEGER, AAWDT FLOAT)')
    conn.close()
    df.to_sql('accidentes_seattle', engine, if_exists='append', index=False)

dag = DAG(
    'accidents_seattle_db_csv',
    default_args=default_args,
    description='Obtener una tabla del número total de accidentes (AAWDT) por calle (STNAME) y año (YEAR)',
    catchup=False
)

# Sensor de archivo
file_sensor_task = FileSensor(
    task_id='file_sensor',
    filepath='https://drive.google.com/u/0/uc?id=1IAb_x49xqjM-8cx-cpHkM1bnR6j-I4T6&export=download',
    poke_interval=360,
    dag=dag
)

# Tarea que lee el archivo CSV
read_csv_task = PythonOperator(
    task_id='read_csv_file',
    python_callable=read_csv_file,
    dag=dag
)

# Tarea que transforma los datos
transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

# Tarea que exporta los datos transformados a un archivo CSV
export_csv_task = PythonOperator(
    task_id='export_csv_data',
    python_callable=export_csv_data,
    dag=dag
)

# Tarea que exporta los datos transformados a una tabla

export_db_task = PostgresOperator(
    task_id='export_db_data',
    postgres_conn_id='postgres_localhost',
    sql='''
        CREATE TABLE IF NOT EXISTS accidentes_seattle (
            STNAME VARCHAR(255),
            YEAR INTEGER,
            AAWDT FLOAT
        );
    ''',
    dag=dag
)
# Tarea para imprimir un mensaje
finish_task = BashOperator(
    task_id='finish_task',
    bash_command='echo "BOX SUCCESS"',
    dag=dag
)

# Dependencias de las tareas
file_sensor_task >> read_csv_task >> transform_data_task >> [export_csv_task, export_db_task] >> finish_task