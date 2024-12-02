import telnetlib
import time

# Configuración de la conexión
HOST = "192.168.22.15"
PORT = 9880
TIMEOUT = 10

# Conectar al dispositivo
tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)

# Función para enviar un comando y obtener la respuesta
def send_command(command):
    tn.write(command.encode('ascii') + b"\r\n")
    time.sleep(1)  # Espera para que el dispositivo procese el comando
    return tn.read_very_eager().decode('ascii')

# Ejemplo de comandos C-Link
commands = [
    "id?",            # Obtener identificación del dispositivo
    "no of lrec",     # Obtener el número de registros largos
    "lrec 0 5"        # Leer los primeros 5 registros largos
]

# Enviar comandos y almacenar respuestas
responses = []
for command in commands:
    response = send_command(command)
    responses.append(response)

# Guardar las respuestas en un archivo
with open("data_output.txt", "w") as file:
    for response in responses:
        file.write(response + "\n")

# Cerrar la conexión Telnet
tn.close()

print("Datos descargados y guardados en 'data_output.txt'")
