import os
from datetime import datetime

def export_data(table, output_path):
    # Guarda la tabla como un archivo CSV 
    table.to_csv(output_path, index=False)

def export_data_with_timestamp(df, output_folder):
    # Crea la carpeta de salida
    os.makedirs(output_folder, exist_ok=True)
    
    # Fecha y hora actual
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    
    # Nombrado de outfile
    output_filename = f"total_accidentes_por_calle_año_{timestamp}.csv"
    
    # Ruta completa de salida
    output_path = os.path.join(output_folder, output_filename)

    # Guardar el DataFrame como un archivo CSV
    df.to_csv(output_path, index=False)