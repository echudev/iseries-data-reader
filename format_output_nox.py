import pandas as pd

# Leer el archivo con una sola columna
df = pd.read_csv('data/data_output_nox.txt', encoding='utf-8', header=None)

# Eliminar las líneas que contienen "lrec" o "sum"
df = df[~df[0].str.contains('lrec|sum', na=False, case=False)]

# Dividir la columna 0 en múltiples columnas
df = df[0].str.split(expand=True)

# Seleccionar solo las columnas 0, 1, 5 y 7
df = df.iloc[:, [0, 1, 5, 7]]

# Convertir las columnas 5 y 7 a tipo float
df[5] = pd.to_numeric(df[5], errors='coerce')
df[7] = pd.to_numeric(df[7], errors='coerce')

# Insertar la nueva columna (resta de columna 7 menos columna 5)
df.insert(loc=3, column='NO2', value=df[7] - df[5])

# Renombrar las columnas 5 y 7
df = df.rename(columns={0: 'HORA', 1: 'FECHA', 5: 'NO', 7: 'NOx'})

# Extraer la hora de la columna 'HORA'
df['HORA'] = df['HORA'].str.split(':').str[0]

# Invertir día y mes en la columna 'FECHA'
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%m-%d-%y').dt.strftime('%Y-%m-%d')

# Agrupar por hora y calcular el promedio
df_promedio = df.groupby(['FECHA', 'HORA'])[['NO', 'NO2', 'NOx']].mean()

# Redondear los valores a números enteros
df_promedio = df_promedio.round(0).astype(int)

# Exportar a Excel
df_promedio.to_excel('data/promedios_nox.xlsx')

print("DataFrame exportado a promedio_nox.xlsx")