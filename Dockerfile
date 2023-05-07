# Airflow mas python
FROM apache/airflow:2.6.0-python3.7

# Copiamos requirements.txt al contenedor
COPY requirements.txt .

# Instalo las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Directorio de trabajo
WORKDIR /app


# Copiamos los archivos necesarios al contenedor
COPY . .

# Establecemos las variables de entorno
ENV AIRFLOW_HOME=/app

# Inicializamos la base de datos de Airflow
RUN airflow db init

# Exponemos el puerto 8080 
EXPOSE 8080

# Comando para iniciar el servidor web de Airflow
CMD ["airflow", "webserver", "-p", "8080"]