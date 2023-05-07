# Aca empezo es donde el proyecto empezo como el sigueinte script. 

import pandas as pd
from datetime import datetime

# Leo el archivo CSV
df = pd.read_csv("fct/Traffic_Flow_Map_Volumes.csv")

# XFR hago la tranformacion requerida y ordeno por nuemro de accidente
result = df.groupby(['STNAME', 'YEAR'])['AAWDT'].sum().reset_index().sort_values(by='AAWDT', ascending=False)

# fecha y hora actual
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H%M%S")

# Nombrado de outfile
output_filename = f"fct/total_accidentes_por_calle_año_{timestamp}.csv"

# Genero un nuevo archivo CSV
result.to_csv(output_filename, index=False)

# imprimo el resultado en una tabla por pantalla
print(result)
