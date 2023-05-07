from extract import read_csv_file

# Función que transforma los datos
def transform_data():
    df = read_csv_file()
    result = df.groupby(['STNAME', 'YEAR'])['AAWDT'].sum().reset_index().sort_values(by='AAWDT', ascending=False)
    result.columns = ['STNAME', 'YEAR', 'AAWDT']
    return result