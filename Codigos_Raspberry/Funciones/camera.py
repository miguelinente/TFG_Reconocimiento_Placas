import time
import datetime
import os
from picamera import PiCamera #type: ignore

# Directorio donde se guardarán las fotos
photo_directory = '/home/raspberry/Desktop/TFG/Codigos_Raspberry/Archivos/fotos'  # Ajusta esta ruta según sea necesario
os.makedirs(photo_directory, exist_ok=True)

# Contador global de fotos
photo_counter = 0

camera = PiCamera()

def hacerfoto():
    global photo_counter
    print('tamos dentro')

    # Incrementar el contador de fotos
    photo_counter += 1

    # Obtener la marca de tiempo actual
    now = datetime.datetime.now()
    timestamp = now.strftime("%M_%H_%d_%m_%Y")

    # Crear el nombre del archivo
    photo_name = f'Placa{photo_counter}_{timestamp}.jpg'
    photo_path = os.path.join(photo_directory, photo_name)

    # Capturar la foto
    camera.capture(photo_path)

    return photo_path
