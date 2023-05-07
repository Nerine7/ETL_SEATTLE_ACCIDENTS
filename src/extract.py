import pandas as pd

def read_csv_file():
    # Path del archivo CSV o sino se puede descargar de esta carpeta drive "https://drive.google.com/u/0/uc?id=1IAb_x49xqjM-8cx-cpHkM1bnR6j-I4T6&export=download"
    file_path = 'fct/Seattle_Traffic_Accidents.csv'
    
    # Lee el archivo CSV con pandas
    df = pd.read_csv(file_path)
    
    # dataframe 
    return df
