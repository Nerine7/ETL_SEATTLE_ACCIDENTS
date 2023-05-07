# ETL_SEATTLE_ACCIDENTS
Este es un pipeline de extracción, transformación y exportación de datos utilizando Apache Airflow y Docker.

   Configuración de Apache Airflow con Docker
1-Instalar Docker en tu máquina local.
2-Crear un Dockerfile que incluya las dependencias requeridas y la configuración para Apache Airflow.
3-Construir y ejecutar el contenedor de Airflow utilizando el Dockerfile.

Si ya tienes todo el repositorio descargado y Docker configurado ejecuta los sigueintes comandos para crear la imagen y levantar el contenedor:
                                    
                                    - docker build -t etl_accidents_seattle .
                                    - docker-compose up


   CARPETA SRC
 En la carpeta src se pueden encontrar varios scripts que se pensaron al inicir el proyecto.
  
  
   Dockerfile
Este archivo es un Dockerfile utilizado para construir una imagen de Docker que incluye Apache Airflow y algunas dependencias Python necesarias. La imagen se crea a partir de la imagen base apache/airflow:2.6.0-python3.7. A continuación, se copia el archivo requirements.txt al contenedor y se instalan las dependencias a través de pip.



El repositorio tiene dos tareas paso a describirlas:



                                                        seatle_csv_dag.py
                                                    (Empece con esta primera task)
                                                    
                                                           Pasos del DAG:  
                                                           
El DAG consta de las siguientes tareas:

1- read_csv_task: Esta tarea lee un archivo CSV desde una URL y devuelve un DataFrame de Pandas con los datos leídos.

2- transform_data_task: Esta tarea toma el DataFrame obtenido por la tarea anterior, realiza algunas transformaciones en los datos (en este caso, agrupa por calle y año y suma el número de accidentes) y devuelve un nuevo DataFrame con los datos transformados.

3- export_data_task: Esta tarea toma el DataFrame obtenido por la tarea anterior y lo exporta a un archivo CSV en el sistema de archivos local. El nombre del archivo incluye la fecha y hora actual en formato YYYY-MM-DD_HHmmSS.

4- finish_task: Esta tarea imprime un mensaje de éxito en la consola.
                                                    
                                                    
                                                        
                                                                                                                
                                                                                                             
                                                        
                                                                                                                                                                  
                                                        seattle_db_csv_dag.py
                                   (Luego de crear la primera task, desarrolle esta que esta mas completa)
                                   
                                                          Pasos del DAG:
El DAG consta de las siguientes tareas:

1- file_sensor_task: un sensor de archivo que verifica si un archivo CSV está disponible para procesar. Este sensor se asegura de que el DAG no comience hasta que el archivo esté disponible para su procesamiento.

2- read_csv_task: esta tarea lee el archivo CSV de una URL remota y devuelve un objeto DataFrame de Pandas.

3- transform_data_task: esta tarea toma el objeto DataFrame devuelto por read_csv_task, lo transforma y lo devuelve como un nuevo DataFrame de Pandas.

4- export_csv_task: esta tarea toma el DataFrame transformado y lo exporta a un archivo CSV. El nombre del archivo incluye la fecha y hora actuales.

5- export_db_task: esta tarea toma el DataFrame transformado y lo exporta a una tabla de base de datos de PostgreSQL.

6- finish_task: esta tarea simplemente imprime un mensaje en la salida estándar para indicar que el DAG ha finalizado con éxito.
  
