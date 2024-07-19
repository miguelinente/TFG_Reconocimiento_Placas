import sys
import time
import RPi.GPIO as GPIO
import os


# Añadir rutas a sys.path
sys.path.append('/home/raspberry/Desktop/TFG/Codigos_Raspberry/Archivos')
sys.path.append('/home/raspberry/Desktop/TFG/Codigos_Raspberry/Funciones')

# Importar módulos personalizados
import camera
print('se importó la función de la camara')

#Coordenadas GPS
latitud=[43.52281597817496,43.52279661890937,43.52276965779678,43.52275253466478,43.52282140882055,43.52280258899841,43.52277165545394,43.52275548544885]
longitud=[-5.628678939002668,-5.628679415839308,-5.628681323043063,-5.628681809088906,-5.628775942996026,-5.628776473229523,-5.628775304243335,-5.628774920769723]

#Setup del GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

boton_inicio=3
boton_foto=5
GPIO.setup(boton_inicio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(boton_foto, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Preparación del archivo de datos
archivo = '/home/raspberry/Desktop/TFG/Codigos_Raspberry/Archivos/Datos_Placas.txt'
with open(archivo, 'w') as file:
    file.write('')

# Variables de control

i = 1

# Esperar el inicio del vuelo
while GPIO.input(boton_inicio)==GPIO.HIGH:
    print("Esperando orden de inicio de vuelo")
    time.sleep(0.1)
print("Se inició el vuelo")

time.sleep(2)

# Realizar operaciones durante el vuelo
while GPIO.input(boton_inicio)==GPIO.HIGH:
    if GPIO.input(boton_foto)==GPIO.LOW:
        if i<9:
            print("Recibí la orden de hacer la foto")
            # Tomar la foto
            photo_path = camera.hacerfoto()
            print('hice la foto')

            with open(archivo, 'a') as file:
                file.write(f'Placa{i},{latitud[i-1]},{longitud[i-1]},{photo_path}\n')
            i += 1  # Incrementar el contador de fotos
        else:
            break    
    else:
        print("Esperando orden para sacar la foto")
        time.sleep(0.1)
print('salí del bucle')


