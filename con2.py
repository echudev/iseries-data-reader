import telnetlib
import time

HOST = "192.168.22.15"
PORT = 9880
TIMEOUT = 10

try:
    # Conectar al dispositivo
    tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)
    print(f"Conectado a {HOST} en el puerto {PORT}")
except ConnectionRefusedError:
    print(f"Conexión rechazada al intentar conectar a {HOST} en el puerto {PORT}")
    exit(1)
except Exception as e:
    print(f"Error al conectar a {HOST} en el puerto {PORT}: {e}")
    exit(1)

# Función para enviar un comando y obtener la respuesta
def send_command(command):
    tn.write(command.encode('ascii') + b"\r\n")
    time.sleep(1)  # Espera para que el dispositivo procese el comando
    return tn.read_very_eager().decode('ascii')

# Obtener el número total de registros largos
total_records_response = send_command("no of lrec")
print(f"Respuesta del comando 'no of lrec': {total_records_response}")

# Extraer el número total de registros de la respuesta
try:
    total_records = int(total_records_response.split()[2])
except (IndexError, ValueError):
    print("Error al interpretar la respuesta del comando 'no of lrec'.")
    tn.close()
    exit(1)

print(f"Número total de registros largos: {total_records}")

# Calcular el punto de inicio para los últimos 100 registros
start_record = max(0, total_records - 100)

# Solicitar los últimos 100 registros
records_response = send_command(f"lrec {start_record} 100")
print(f"Respuesta del comando 'lrec {start_record} 100': {records_response}")

# Guardar las respuestas en un archivo
with open("data_output.txt", "w") as file:
    file.write(records_response)

# Cerrar la conexión Telnet
tn.close()

print("Datos descargados y guardados en 'data_output.txt'")
