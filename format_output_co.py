import pandas as pd
from pathlib import Path

# Archivo de entrada y salida
INPUT_PATH = Path('data') / 'data_output_co.txt'
OUTPUT_PATH = Path('data') / 'co_datetime.xlsx'

rows = []

with INPUT_PATH.open('r', encoding='utf-8') as fh:
	for line in fh:
		line = line.strip()
		if not line:
			continue
		low = line.lower()
		# Omitir líneas de control
		if 'lrec' in low or low.startswith('sum') or low.startswith('*'):
			continue
		# Quitar caracteres problemáticos como asterisco final
		clean = line.replace('*', '')
		tokens = clean.split()
		# Esperamos al menos hora y fecha
		if len(tokens) < 3:
			continue
		time_token = tokens[0]
		date_token = tokens[1]

		# Buscar el token 'co' y su valor siguiente
		try:
			i = [t.lower() for t in tokens].index('co')
			co_val = tokens[i+1]
		except (ValueError, IndexError):
			# Línea sin 'co' o malformada
			continue

		# Limpiar el valor y convertir a número
		try:
			co_num = float(co_val)
		except ValueError:
			# intentar limpiar comas o caracteres
			co_num = pd.to_numeric(co_val.replace(',', ''), errors='coerce')
			if pd.isna(co_num):
				continue

		# Normalizar fecha mm-dd-yy -> YYYY-MM-DD
		try:
			date_parsed = pd.to_datetime(date_token, format='%m-%d-%y')
		except Exception:
			# intentar inferir con coerción
			date_parsed = pd.to_datetime(date_token, errors='coerce')
			if pd.isna(date_parsed):
				continue

		# Combinar fecha y hora (hora viene en formato HH:MM)
		datetime_str = f"{date_parsed.strftime('%Y-%m-%d')} {time_token}"

		rows.append({'FECHA_HORA': datetime_str, 'CO': co_num})

if not rows:
	print(f"No se encontraron registros válidos en {INPUT_PATH}")
else:
	df = pd.DataFrame(rows)
	# Convertir FECHA_HORA a datetime real
	df['FECHA_HORA'] = pd.to_datetime(df['FECHA_HORA'], format='%Y-%m-%d %H:%M', errors='coerce')
	# Ordenar
	df = df.sort_values('FECHA_HORA')
	# Exportar a Excel
	df.to_excel(OUTPUT_PATH, index=False)
	print(f"Exportado {len(df)} filas a {OUTPUT_PATH}")