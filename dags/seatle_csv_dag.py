import os
import pandas as pd
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import airflow

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
def export_data():
    df = transform_data()
    
    # Fecha y hora actual
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    
    # Nombrado de outfile
    output_filename = f"total_accidentes_por_calle_año_{timestamp}.csv"

    # Genero archivo CSV
    df.to_csv(output_filename, index=False)

dag = DAG(
    'accidents_by_street_and_year',
    default_args=default_args,
    description='Obtener una tabla del número total de accidentes (AAWDT) por calle (STNAME) y año (YEAR)',
    catchup=False
)

# Tarea para leer el archivo CSV
read_csv_task = PythonOperator(
    task_id='read_csv',
    python_callable=read_csv_file,
    dag=dag
)

# Tarea para transformar los datos
transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

# Tarea para exportar los datos transformados a un archivo CSV
export_data_task = PythonOperator(
    task_id='export_data',
    python_callable=export_data,
    dag=dag
)

# Tarea para imprimir un mensaje 
finish_task = BashOperator(
    task_id='finish_task',
    bash_command='echo "BOX SUCCESS"',
    dag=dag
)

# Dependencias de las tareas
read_csv_task >> transform_data_task >> export_data_task >> finish_task